from kivy.core.image import Image as CoreImage
import common_var
texture_add_to_question = CoreImage('uix_images/tech_texture.jpg').texture
texture_of_tech = CoreImage('uix_images/tech_texture.jpg').texture

texture_medals = CoreImage("different_images/medals.jpg").texture

texture_questions = CoreImage("different_images/questions.jpg").texture

error_texture = CoreImage("different_images/error.jpg").texture
tex_gold_res = CoreImage("different_images/gold_res.jpg").texture
tex_ramka = CoreImage("different_images/ramka.jpg").texture
texture_locked = CoreImage('tech_images/locked_tech.jpg').texture

texture_respirator = CoreImage("tech_images/respirator.jpg").texture
textures_of_tech = ["a"]*common_var.QUANT_OF_TECH

tech_im_names = ["00_production", "01_hospitals", "09_science_communication",
                 "03_masks_and_gloves", "04_airline_cancelling", "05_reducing_of_communication",
                 "06_isolate", "07_hard_carantin", "08_mass_tests", 
                 "09_science_communication", "10_vaccine", "11_cure",
                 "12_distant.png", "13_propaganda.png", "14_udalenka.png",
                 "15_emission.png", "16_goscompany.png", "17_taxes.png",
                 "18_embargo.jpg", "19_corruption.jpg", "20_transferts.jpg",
                 "21_distortion.jpg", "22_automat.jpg", "23_optim.jpg",
                 "24_import_ill.jpg", "25_plazma.jpg", "26_laws.jpg",
                 "27_persuasion.jpg", "02_nii", "09_science_communication",
                 "30_hum_aid.jpg", "31_healthy.jpg"]

for i in range(len(tech_im_names)):
    tech_im_names[i] = "tech_images/" + tech_im_names[i]
    textures_of_tech[i] = CoreImage(tech_im_names[i]).texture

