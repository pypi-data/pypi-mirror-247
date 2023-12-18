# !/usr/bin/python
# coding=utf-8
try:
    import pymel.core as pm
except ImportError as error:
    print(__file__, error)
import mayatk as mtk
from tentacle.slots.maya import SlotsMaya


class Materials(SlotsMaya):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = self.sb.materials
        self.submenu = self.sb.materials_submenu

    def header_init(self, widget):
        """ """
        # Add a button to launch the hdr manager.
        widget.menu.add(
            self.sb.PushButton,
            setToolTip="Manage the scene's HDR shader.",
            setText="HDR Manager",
            setObjectName="b000",
        )
        module = mtk.mat_utils.hdr_manager
        slot_class = module.HdrManagerSlots

        self.sb.register("hdr_manager.ui", slot_class, base_dir=module)
        widget.menu.b000.clicked.connect(lambda: self.sb.parent().set_ui("hdr_manager"))

        # Add a button to launch stringray arnold shader.
        widget.menu.add(
            self.sb.PushButton,
            setToolTip="Create a stingray material network that can be previewed in Arnold.",
            setText="Stingray Arnold Shader",
            setObjectName="b001",
        )
        module = mtk.mat_utils.stingray_arnold_shader
        slot_class = module.StingrayArnoldShaderSlots

        self.sb.register("stingray_arnold_shader.ui", slot_class, base_dir=module)
        widget.menu.b001.clicked.connect(
            lambda: self.sb.parent().set_ui("stingray_arnold_shader")
        )

    def cmb000_init(self, widget):
        """ """
        # Get all shader types derived from the 'shader' class
        items = pm.listNodeTypes("shader")
        widget.add(items, header="Assign New", header_alignment="center")

    def cmb000(self, index, widget):
        """Assign: Assign New"""
        selection = pm.ls(sl=True, flatten=1)
        if not selection:
            self.sb.message_box("No renderable object is selected for assignment.")
            return

        mat_name = widget.itemText(index)
        mat = mtk.create_mat(mat_name)
        mtk.assign_mat(selection, mat)
        self.ui.cmb002.init_slot()
        self.ui.cmb002.setAsCurrent(mat_name)

    def cmb002_init(self, widget):
        """ """
        widget.refresh = True
        if not widget.is_initialized:
            widget.editable = True
            widget.menu.mode = "context"
            widget.menu.setTitle("Material Options")
            widget.menu.add(
                self.sb.Label,
                setText="Select",
                setObjectName="lbl004",
                setToolTip="Select the material and show its attributes in the attribute editor.",
            )
            widget.menu.add(
                self.sb.Label,
                setText="Rename",
                setObjectName="lbl005",
                setToolTip="Rename the current material.",
            )
            widget.menu.add(
                self.sb.Label,
                setText="Reload Textures",
                setObjectName="lbl006",
                setToolTip="Reload textures for all scene materials.",
            )
            widget.menu.add(
                self.sb.Label,
                setText="Delete",
                setObjectName="lbl002",
                setToolTip="Delete the current material.",
            )
            widget.menu.add(
                self.sb.Label,
                setText="Delete All Unused Materials",
                setObjectName="lbl003",
                setToolTip="Delete All unused materials.",
            )
            widget.menu.add(
                self.sb.Label,
                setText="Open in Editor",
                setObjectName="lbl000",
                setToolTip="Open the current material in editor.",
            )
            # Rename the material after editing has finished.
            widget.on_editing_finished.connect(
                lambda text: pm.rename(widget.currentData(), text)
            )
            # Update the assign button with the new material name.
            widget.on_editing_finished.connect(self.ui.b005.init_slot)
            # Initialize the widget every time before the popup is shown.
            widget.before_popup_shown.connect(widget.init_slot)
            # Add the current material name to the assign button.
            widget.currentIndexChanged.connect(self.ui.b005.init_slot)

        # Use 'restore_index=True' to save and restore the index
        materials = mtk.get_scene_mats(exc="standardSurface")
        materials_dict = {m.name(): m for m in materials}
        widget.add(materials_dict, clear=True, restore_index=True)

        # Create and set icons with color swatch
        for i, mat in enumerate(widget.items):
            icon = mtk.get_mat_swatch_icon(mat)
            if icon:
                widget.setItemIcon(i, icon)

    def tb000_init(self, widget):
        """ """
        widget.menu.add(
            "QCheckBox",
            setText="Shell",
            setObjectName="chk005",
            setToolTip="Select object(s) containing the material.",
        )

    def tb000(self, widget):
        """Select By Material ID"""
        mat = self.ui.cmb002.currentData()
        if not mat:
            self.sb.message_box(
                amg="<hl>Nothing selected</hl><br>Select an object face, or choose the option: current material.",
                pos="midCenterTop",
                fade=True,
            )
            return

        shell = widget.menu.chk005.isChecked()  # Select by material: shell

        selection = pm.ls(sl=True, objectsOnly=True)
        faces_with_mat = mtk.find_by_mat_id(mat, selection, shell=shell)

        pm.select(faces_with_mat)

    def lbl000(self):
        """Open material in editor"""
        try:
            mat = self.ui.cmb002.currentData()
            pm.select(mat)
        except Exception:
            self.sb.message_box("No stored material or no valid object selected.")
            return

        pm.mel.HypershadeWindow()
        #  Finally, graph the material in the hypershade window.
        pm.mel.eval(
            'hyperShadePanelGraphCommand("hyperShadePanel1", "showUpAndDownstream")'
        )

    def lbl002(self):
        """Delete Material"""
        mat = self.ui.cmb002.currentData()  # get the mat obj from cmb002
        mat = pm.delete(mat)
        self.ui.cmb002.init_slot()  # refresh the materials list comboBox

    def lbl003(self, widget):
        """Delete Unused Materials"""
        pm.mel.hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes")
        self.ui.cmb002.init_slot()  # refresh the materials list comboBox

    def lbl004(self):
        """Select and Show Attributes: Show Material Attributes in the Attribute Editor."""
        mat = self.ui.cmb002.currentData()  # get the mat obj from cmb002
        pm.select(mat, replace=True)
        pm.mel.eval(f'showEditorExact("{mat}")')

    def lbl005(self):
        """Set the current combo box text as editable."""
        self.ui.cmb002.setEditable(True)
        self.ui.cmb002.menu.hide()

    def lbl006(self):
        """Reload Textures"""
        mtk.reload_textures()
        confirmation_message = "<html><body><p style='font-size:16px; color:yellow;'>Textures have been <strong>reloaded</strong>.</p></body></html>"
        self.sb.message_box(confirmation_message)

    def b002(self, widget):
        """Get Material: Change the index to match the current material selection."""
        selection = pm.ls(sl=True)
        if not selection:
            self.sb.message_box(
                "<hl>Nothing selected</hl><br>Select mesh object(s) or face(s)."
            )
            return

        mat = mtk.get_mats(selection[0])
        if len(mat) != 1:
            self.sb.message_box(
                "<hl>Invalid selection</hl><br>Selection must have exactly one material assigned."
            )
            return

        self.ui.cmb002.init_slot()  # refresh the materials list comboBox
        self.ui.cmb002.setAsCurrent(mat.pop().name())  # pop: mat is a set

    def b004(self, widget):
        """Assign: Assign Random"""
        selection = pm.ls(sl=True, flatten=1)
        if not selection:
            self.sb.message_box("No renderable object is selected for assignment.")
            return

        mat = mtk.create_mat("random")
        mtk.assign_mat(selection, mat)

        self.ui.cmb002.init_slot()  # refresh the materials list comboBox
        self.ui.cmb002.setAsCurrent(mat.name())

    def b005_init(self, widget):
        """ """
        widget.refresh = True
        current_material = self.ui.cmb002.currentData()
        text = f"Assign: {current_material}"
        submenu_widget = self.submenu.b005
        submenu_widget.setText(text)
        submenu_widget.setMinimumWidth(submenu_widget.minimumSizeHint().width() + 25)
        if current_material:
            icon = mtk.get_mat_swatch_icon(current_material, [15, 15])
            if icon is not None:
                submenu_widget.setIcon(icon)

    def b005(self, widget):
        """Assign: Assign Current"""
        selection = pm.ls(sl=True, flatten=1)
        if not selection:
            self.sb.message_box("No renderable object is selected for assignment.")
            return

        mat = self.ui.cmb002.currentData()
        mtk.assign_mat(selection, mat)


# --------------------------------------------------------------------------------------------

# module name
# print(__name__)
# --------------------------------------------------------------------------------------------
# Notes
# --------------------------------------------------------------------------------------------
