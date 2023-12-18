# !/usr/bin/python
# coding=utf-8
import sys
from PySide2 import QtCore, QtGui, QtWidgets


class OverlayFactoryFilter(QtCore.QObject):
    """This class provides an event filter to relay events from the parent widget to the overlay."""

    def eventFilter(self, widget, event):
        """Relay events from the parent widget to the overlay.
        Captures various event types and forwards them to the respective methods.

        Parameters:
            widget (QWidget): The parent widget that the event filter is applied to.
            event (QEvent): The event that needs to be processed.

        Returns:
            bool: False if the widget is not a QWidget, True otherwise.
        """
        if not widget.isWidgetType():
            return False

        if event.type() == QtCore.QEvent.MouseButtonPress:
            self.mousePressEvent(event)

        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            self.mouseReleaseEvent(event)

        elif event.type() == QtCore.QEvent.MouseMove:
            self.mouseMoveEvent(event)

        elif event.type() == QtCore.QEvent.MouseButtonDblClick:
            self.mouseDoubleClickEvent(event)

        elif event.type() == QtCore.QEvent.KeyPress:
            self.keyPressEvent(event)

        elif event.type() == QtCore.QEvent.KeyRelease:
            self.keyReleaseEvent(event)

        elif event.type() == QtCore.QEvent.Resize:
            if widget == self.parentWidget():
                self.resize(widget.size())

        elif event.type() == QtCore.QEvent.Show:
            self.raise_()

        return super().eventFilter(widget, event)


class Path:
    """The Path class represents a sequence of widget positions and cursor positions
    that can be navigated. It is used in conjunction with the Overlay class to
    visually represent a path on a GUI.

    Attributes:
        _path: A list of tuples, where each tuple contains a widget reference,
               the global position of the widget's center, and the global cursor
               position at the time of adding.
    """

    def __init__(self):
        """Initializes a new instance of the Path class."""
        self._path = []

    def __iter__(self):
        """Special method to allow iteration."""
        return iter(self._path)

    def __getitem__(self, index):
        """Special method to allow indexed access."""
        return self._path[index]

    def __setitem__(self, index, value):
        """Special method to allow indexed assignment."""
        self._path[index] = value

    def __repr__(self):
        """Provides a string representation of the current path."""
        return f"Path({self._path})"

    @property
    def start_pos(self) -> QtCore.QPoint:
        """Gets the starting position of the path.

        Returns:
            The cursor position when the path was first created, or None if the
            path is empty.
        """
        try:
            return self._path[0][2]
        except IndexError:
            return None

    @property
    def widget_positions(self) -> dict:
        """Gets the global position of the center of a specific widget in the path.

        Parameters:
            target_widget: The widget to find the position of.

        Returns:
            The global position of the center of the target_widget,
            or None if the widget is not found in the path.
        """
        return {widget: widget_pos for widget, widget_pos, _ in self._path[1:]}

    def widget_position(self, target_widget):
        """Gets the global position of the center of a specific widget in the path.

        Parameters:
            target_widget: The widget to find the position of.

        Returns:
            The global position of the center of the target_widget,
            or None if the widget is not found in the path.
        """
        return next(
            (
                widget_pos
                for widget, widget_pos, _ in self._path
                if widget == target_widget
            ),
            None,
        )

    def reset(self):
        """Clears the path and appends the current cursor position as the new starting position."""
        self.clear()
        curPos = QtGui.QCursor.pos()
        self._path.append((None, None, curPos))

    def clear(self):
        """Clears the entire path."""
        self._path.clear()

    def clear_to_origin(self):
        """Clears the path but retains the original starting position."""
        self._path = self._path[:1]

    def add(self, ui, widget):
        """Adds a widget and its position to the path. Also removes any references
        to the provided ui object from the path.

        Parameters:
            ui: The ui object to remove from the path.
            widget: The widget to add to the path.
        """
        w_pos = widget.mapToGlobal(widget.rect().center())
        self._path.append((widget, w_pos, QtGui.QCursor.pos()))
        self.remove(ui)

    def remove(self, target_ui):
        """Removes all references to the provided ui object from the path.
        Preserves the portion of the path up to and including the last occurrence
        of the target_ui.

        Parameters:
            target_ui: The ui object to remove from the path.
        """
        last_occurrence_index = next(
            (
                index + 1
                for index, (widget, _, _) in reversed(list(enumerate(self._path[1:])))
                if widget.ui == target_ui
            ),
            None,
        )
        if last_occurrence_index is not None:
            self._path = self._path[:last_occurrence_index]
        else:
            self._path = self._path[:]


class Overlay(QtWidgets.QWidget, OverlayFactoryFilter):
    """Handles paint events as an overlay on top of an existing widget.
    Inherits from OverlayFactoryFilter to relay events from the parent widget to the overlay.
    Maintains a list of draw paths to track the user's interactions.

    Parameters:
        parent (QWidget, optional): The parent widget for the overlay. Defaults to None.
        antialiasing (bool, optional): Set antialiasing for the tangent paint events. Defaults to False.
    """

    # return the existing QApplication object, or create a new one if none exist.
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    def __init__(self, parent=None, antialiasing=False):
        super().__init__(parent)

        self.antialiasing = antialiasing
        self.draw_enabled = False
        self.clear_painting = False

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self.fg_color = QtGui.QColor(115, 115, 115)
        self.bg_color = QtGui.QColor(127, 127, 127, 0)
        self.pen_color = QtGui.QPen(
            self.fg_color,
            3,
            QtCore.Qt.SolidLine,
            QtCore.Qt.RoundCap,
            QtCore.Qt.RoundJoin,
        )
        self.pen_stroke = QtGui.QPen(
            QtGui.QColor(0, 0, 0),
            2,
            QtCore.Qt.SolidLine,
            QtCore.Qt.RoundCap,
            QtCore.Qt.RoundJoin,
        )

        self.painter = QtGui.QPainter()
        self.path = Path()

        if parent:
            parent.installEventFilter(self)

    def draw_tangent(self, start_point, end_point, ellipseSize=7):
        """Draws a tangent line between two points with an ellipse at the start point.

        Parameters:
            start_point (QtCore.QPointF): The starting point of the line.
            end_point (QtCore.QPointF): The ending point of the line.
            ellipseSize (int, optional): The size of the ellipse at the starting point. Defaults to 7.
        """
        if end_point.isNull():
            return

        linePath = QtGui.QPainterPath()
        ellipsePath = QtGui.QPainterPath()

        if ellipseSize:
            ellipsePath.addEllipse(start_point, ellipseSize, ellipseSize)

        self.painter.fillRect(self.rect(), self.bg_color)
        self.painter.setRenderHint(QtGui.QPainter.Antialiasing, self.antialiasing)

        # Draw the line
        linePath.moveTo(start_point)
        linePath.lineTo(end_point)

        # Combine the paths
        combinedPath = QtGui.QPainterPath()
        combinedPath.addPath(ellipsePath)
        combinedPath.addPath(linePath)

        # Create a stroker with the pen_stroke and stroke the combined path
        stroker = QtGui.QPainterPathStroker(self.pen_stroke)
        strokedPath = stroker.createStroke(combinedPath)

        # Draw the stroked path (outline)
        self.painter.setPen(self.pen_stroke)
        self.painter.setBrush(QtCore.Qt.NoBrush)
        self.painter.drawPath(strokedPath)

        # Draw the combined shape with the fill color
        self.painter.setPen(self.pen_color)
        self.painter.setBrush(self.fg_color)
        self.painter.drawPath(combinedPath)

    def init_region(self, ui, *args, **kwargs):
        """Initializes a Region widget with the specified properties and adds it to the given UI's central widget.

        Parameters:
            ui (QWidget): The parent QWidget in which the Region widget will be added.

        Returns:
            Region: The initialized Region widget.
        """
        from uitk.widgets.region import Region

        region_widget = Region(ui, *args, **kwargs)

        return region_widget

    def clone_widgets_along_path(self, ui, return_func):
        """Re-constructs the relevant widgets from the previous UI for the new UI, and positions them.
        Initializes the new widgets by adding them to the switchboard.
        The previous widget information is derived from the widget and draw paths.
        Sets up the on_enter signal of the Region widget to be connected to the return_to_start method.

        Parameters:
            ui (QMainWindow): The UI in which to copy the widgets to.
        """
        if not self.path.start_pos:
            raise ValueError("No start position found in the path.")

        # Initialize the return area region for the UI
        region_widget = self.init_region(ui, self.path.start_pos)
        region_widget.on_enter.connect(return_func)
        region_widget.on_enter.connect(self.path.clear_to_origin)

        # Clone the widgets along the path. Omit the starting index and the last widget which already exists in the new UI.
        to_clone = self.path._path[1:-1]
        new_widgets = tuple(self._clone_widget(ui, w, pos) for w, pos, _ in to_clone)

        return new_widgets

    def _clone_widget(self, ui, prev_widget, position):
        """Clone a widget and place it on the given position in the UI.

        Parameters:
            ui (QMainWindow): The UI to place the cloned widget.
            prev_widget (QWidget): The widget to clone.
            position (QPoint): The position to place the cloned widget.
        """
        new_widget = type(prev_widget)(ui)

        try:
            new_widget.setObjectName(prev_widget.objectName())
            new_widget.resize(prev_widget.size())
            new_widget.setWhatsThis(prev_widget.whatsThis())
            new_widget.setText(prev_widget.text())
            new_widget.move(  # set the position of the new widget in the new UI.
                new_widget.mapFromGlobal(position - new_widget.rect().center())
            )
            new_widget.setVisible(True)
        except AttributeError:
            pass

        return new_widget

    def clear_paint_events(self):
        """Clear paint events by disabling drawing and updating the overlay."""
        self.clear_painting = True
        self.update()

    def paintEvent(self, event):
        """Handles the paint event for the overlay, drawing the tangent paths as needed."""
        self.painter.begin(self)

        if self.clear_painting:
            self.painter.fillRect(self.rect(), self.bg_color)
            self.clear_painting = False
        elif self.draw_enabled:
            # plot and draw the points in the path list.
            for i, (_, _, start_point) in enumerate(self.path._path):
                start_point = self.mapFromGlobal(start_point)
                try:
                    end_point = self.mapFromGlobal(self.path._path[i + 1][2])
                except IndexError:
                    end_point = self.mouseMovePos
                    # after the list points are drawn, plot the current end_point, controlled by the mouse move event.

                self.draw_tangent(start_point, end_point)

        self.painter.end()

    def mousePressEvent(self, event):
        """ """
        # Change the cursor shape to a drag move cursor.
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))

        self.clear_paint_events()
        self.path.reset()
        self.mouseMovePos = event.pos()

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """ """
        # Restore the cursor to its default shape.
        QtWidgets.QApplication.restoreOverrideCursor()

        self.clear_paint_events()  # Explicitly clear the overlay

        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        """ """
        self.draw_enabled = True
        self.mouseMovePos = event.pos()
        self.update()

        super().mouseMoveEvent(event)

    def hideEvent(self, event):
        """Clears the path and restores the cursor to its default shape when the overlay is hidden."""
        self.path.clear()
        QtWidgets.QApplication.restoreOverrideCursor()  # Restore the cursor to its default shape.
        super().hideEvent(event)


# --------------------------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    overlay = Overlay()

    sys.exit(overlay.app.exec_())

# module name
# print(__name__)
# --------------------------------------------------------------------------------------------
# Notes
# --------------------------------------------------------------------------------------------
