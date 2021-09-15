import sys
import bpy
from collections import OrderedDict
from itertools import repeat
import pprint
import pdb
from bpy.types import Operator, Panel
from bpy.props import (
    IntProperty,
)
from copy import copy

class FileOutputNode(Panel):
    bl_label = "File Output Node"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Compositing Nodes"

    def draw(self, context):
        if context.active_node is not None:
            layout = self.layout
            row = layout.row()
            col = layout.column

            row = layout.row()
            row.operator('node.button_rename', text="Rename")

class FO_OT_RenameInputs(Operator):
    bl_idname = 'node.button_rename'
    bl_label = 'Rename'

    def execute(self, context):
        nodes = get_fileOutputNodes(context)
        for node in nodes:
            node.base_path = "//" + py.path.basename(bpy.context.blend_data.filepath)
            for i in range(len(node.inputs)):
               if(len(node.inputs[i].links) > 0):
                   nodeFromName = node.inputs[i].links[0].from_node.name
                   socketFromName = node.inputs[i].links[0].from_socket.name
                   node.file_slots[i].path = nodeFromName + '_' + socketFromName
        return {'FINISHED'}

def get_fileOutputNodes(context):
    tree = context.scene.node_tree
    sel = [x for x in tree.nodes if x.bl_idname == "CompositorNodeOutputFile"] 
    return sel


classes = [
     FO_OT_RenameInputs,
     FileOutputNode
]

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()

