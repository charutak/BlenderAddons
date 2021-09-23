bl_info = {
    "name": "File Output Node Rename Button",
    "author": "Charu Tak",
    "version": (1, 0, 0),
    "blender": (2, 93, 0),
    "location": "Compositor's Header",
    "description": "Renames input sockets for file output node based on the links.",
    "wiki_url": "",
    "category": "Node"}

import bpy

class FILEOUTPUT_OT_BUTTON(bpy.types.Operator):
    bl_idname = "fileoutput.rename"
    bl_label = "Rename"
    bl_description = "Rename file output node's input sockets."
    bl_options = {"REGISTER"}

    def execute(self, context):
        nodes = get_fileOutputNodes(context)
        fileName = bpy.path.basename(bpy.context.blend_data.filepath)
        fileName = fileName.split('.')[0]

        for node in nodes:
            for i in range(len(node.inputs)):
               if(len(node.inputs[i].links) > 0):
                   nodeFromName = node.inputs[i].links[0].from_node.name
                   if(node.inputs[i].links[0].from_node.label != ''):
                       nodeFromName = node.inputs[i].links[0].from_node.label

                   socketFromName = node.inputs[i].links[0].from_socket.name
                   finalSocketName = nodeFromName + '_' + socketFromName
                   node.file_slots[i].path = finalSocketName + '\\' + fileName + "_" + finalSocketName + "_"

        return {'FINISHED'}


def draw(self, context):
    self.layout.operator(FILEOUTPUT_OT_BUTTON.bl_idname)   

def get_fileOutputNodes(context):
    tree = context.scene.node_tree
    sel = [x for x in tree.nodes if x.bl_idname == "CompositorNodeOutputFile"]
    return sel


classes = [
     FILEOUTPUT_OT_BUTTON,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.NODE_HT_header.append(draw)

def unregister():
    bpy.types.NODE_HT_header.remove(draw)
    for c in classes:
        bpy.utils.unregister_class(c)
     

if __name__ == "__main__":
    register()

