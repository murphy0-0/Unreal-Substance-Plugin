from unreal import (AssetToolsHelpers,AssetTools,EditorAssetLibrary,Material,MaterialFactoryNew,MaterialProperty,MaterialEditingLibrary,MaterialExpressionTextureSampleParameter2D as TexSample2D,
                    AssetImportTask,FbxImportUI, Texture2D, StaticMesh, StaticMaterial, MaterialInstance, MaterialInstanceConstantFactoryNew, StringLibrary)
#imports unreal into python
import os 
#imports operating system

class UnrealUtiity: #organizes subfolder for materials in content drawer
    def __init__(self): #makesn object in unreal utility
        self.substanceRootDir = "/game/Substance/" #makes folder for substance
        self.baseMaterialsName = "M_SubstanceBase" #makse folder for base materials
        self.substanceTempDir = "/game/Substance/Temp/" #makes temporary folder

        self.baseMaterialPath = self.substanceRootDir + self.baseMaterialsName #substance base name in substance root directory
        self.baseColorName = "BaseColor" #base color name
        self.occRoughnessMetalicName = "OcclusionRoughnessMetalic" #rough, metalic, and ao name
        self.normalName = "Normal" #normal map name
    def FindOrCreateBaseMaterial(self): #checks for base material
        if EditorAssetLibrary.does_asset_exist(self.baseMaterialPath): #checks if base material exists in unreal content drawer
            return EditorAssetLibrary.load_asset(self.baseMaterialPath) #return if exists
        
        baseMat = AssetToolsHelpers.get_asset_tools().create_asset(self.baseMaterialsName,self.substanceRootDir,Material,MaterialFactoryNew())

        baseColor = MaterialEditingLibrary.create_material_expression(baseMat,TexSample2D,-800,0) #makes normal expression on material for basecolor 
        baseColor.set_editor_property("parameter_name",self.baseColorName) #finds base color
        MaterialEditingLibrary.connect_material_property(baseColor, "RGB", MaterialProperty.MP_BASE_COLOR) #connects in node editor (base color of basecolor map to material)

        normal = MaterialEditingLibrary.create_material_expression(baseMat,TexSample2D,-800,400) #makes normal expression on material for normal map
        normal.set_editor_propery("parameter name", self.normalName) #finds normal map
        normal.set_editor_property("texture", EditorAssetLibrary.load_asset("/Engine/EngineMaterials/DefaultNormal")) #uses texture in unreal materials for normal
        MaterialEditingLibrary.connect_material_property(normal, "RGB", MaterialProperty.MP_NORMAL) #connects normal map in material

        occRoughnessMetalic = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800,800) #makes roughness, metalic, and ao expression for material
        occRoughnessMetalic.set_editor_property("parameter name", self.occRoughnessMetalicName) #finds occroughnessmetalic name
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "R", MaterialProperty.MP_AMBIENT_OCCLUSION) #connects ambient occlusion in R in material
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "G", MaterialProperty.MP_ROUGHNESS) #connects roughness in  G in material
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic,"B", MaterialProperty.MP_METALLIC) #connects metallic in  B in material

        EditorAssetLibrary.save_asset(baseMat.get_path_name()) #saves asset within same location
        return baseMat #returns base material
    
    def LoadMeshFromPath(self,meshPath): #loads mesh using meshpath
        meshName = os.path.split(meshPath)[-1].replace(".fbx","")  #extracts/names mesh
        importTask = AssetImportTask() #import will import to unreal
        importTask.replace_existing = True #if import exists, will replace it
        importTask.filename = meshPath #import name
        importTask.destination_path = "/game/" + meshName #where import will be stored
        importTask.save = True # import saved
        importTask.automated = True  #runs automatically

        fbxImportOptions = FbxImportUI() #Import UI of fbx file when fbx is loading
        fbxImportOptions.import_mesh = True #enables import of the mesh from the fbx 
        fbxImportOptions.import_as_skeletal = False #disables import skeletal from  fbx  
        fbxImportOptions.import_materials = False #disables import materials from fbx 
        fbxImportOptions.static_mesh_import_data.combine_meshes = True #Import mesh data and combined meshes when fbx file is loaded

        importTask.options = fbxImportOptions #imported task = imported fbx

        AssetToolsHelpers.get_asset_tools().import_asset_tasks([importTask]) #uses asset tools to create objects via import task
        return importTask.get_objects()[0] #returns objects created
    
    def LoadTextureFromPath(self, texturePath):
        importTask = AssetImportTask() #import will import to unreal
        importTask.replace_existing = True #if import exists, will replace it
        importTask.filename = texturePath #import name
        importTask.destination_path =self.substanceTempDir #where import will be stored
        importTask.save = True # import saved

        AssetToolsHelpers.get_asset_tools().import_asset_tasks([importTask]) #uses asset tools to create objects via import task
        return importTask.get_objects()[0] #returns objects created

    def LoadFromDir(self,fileDir): #loads from directory
        meshes = []
        textures = []
        for file in os.listdir(fileDir): #finds file in list from directory
            if ".fbx" in file: #finds fbx within files
                self.LoadMeshFromPath(os.path.join(fileDir,file)) #if fbx file is found, it adds it to file directory path
            else:
                textures.append(self.LoadTextureFromPath(os.path.join(fileDir, file)))

        for mesh in meshes:
            self.BuildMaterialForMesh(meshes, textures)

    def NuildMaterialFoMesh(self, mesh: StaticMesh, textures: list[Texture2D]):
        meshName = mesh.get_name()
        meshDir = '/game/' + meshName + "/"
        materialsDir = meshDir + "Materials/"

        if EditorAssetLibrary.does_directory_exist(materialsDir):
            EditorAssetLibrary.delete_directory(materialsDir)

        for index, staticMaterialSlot in enumerate(mesh.static_materials):
            staticMaterialSlot: StaticMaterial = staticMaterialSlot
            materialSlotNameStr = StringLibrary.conv_name_to_string(staticMaterialSlot.material_slot_name)

            baseColor = None
            normal = None
            occRoughnessMetalic = None
            for texture in textures:
                if meshName not in texture.get_name() or materialSlotNameStr not in texture.get_name():
                    continue

            if self.baseColorName in texture.get_name():
                baseColor = texture

            if self.normalName in texture.get_name():
                normal = texture

            if self.occRoughnessMetalicName in texture.get_name():
                occRoughnessMetalic = texture

                