from os import walk

import pygame

surf = pygame.surface

def import_folder(path):

    surface_list = []

    for _,__,img_files in walk(path):

        for image in img_files:

            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()

            surface_list.append(image_surf)

    return surface_list



        
        
# Here you cannot have anything else inside your folder bc then pygame 
# will try to put it in a folder.


