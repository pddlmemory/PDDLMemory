(define (problem appartment-problem)
   
   (:domain appartment)
   
   (:objects 	
              ; Bathroom locations
              shower towel_holder
              bathroom_mirror bathroom_sink 
              bathroom_cabinet - Location
              bathroom_lamp - Lamp
              bathroom_floor - Floor
              bathroom_window - Window
              bathroom_lightswitch - Lightswitch

              ; Bathroom objects
              ba_soap shampoo towel1 towel2 - MovableObject
              lightbulb1 - Lightbulb

              ; ***************************

              ; WC locations
              toilet wc_sink - Location
              wc_window - Window
              wc_lightswitch - Lightswitch
              wc_lamp - Lamp
              wc_floor - Floor

              ; WC facts
              toilet_paper wc_wastebin
              wc_soap - MovableObject
              lightbulb2 - Lightbulb

              ; ***************************

              ; Closet locations
              closet_cabinet - Location
              closet_floor - Floor

              ; Closet objects
              vacuum_cleaner - MovableObject
              lightbulb3 lightbulb4 - Lightbulb
              cleaning_products - CleaningProducts

              ; ***************************

              ; Kitchen locations
              fridge oven waterboiler
              plot1 plot2 dish_rack hotplates
              ki_table ki_cabinet1 ki_sink ki_cabinet2 
              ki_left_drawer ki_right_drawer ki_garbage - Location
              ki_floor - Floor
              ki_lamp - Lamp
              ki_lightswitch - Lightswitch
              ki_window - Window

              ; Kitchen objects
              fruit_tea waterpot teapot
              big_cup cup1 cup2 cup3 cup4 
              small_spoon1 small_spoon2 
              small_spoon3 small_spoon4 - MovableObject
              lightbulb7 - Lightbulb
              
              ; ***************************

              ; Corridor locations
              shoe_cabinet coat_stand co_garbage - Location
              co_lamp - Lamp
              co_lightswitch - Lightswitch
              co_floor - Floor

              ; Corridor objects
              shoepair1 shoepair2 shoepair3 - MovableObject
              lightbulb5 - Lightbulb

              ; ***************************

              ; Bedroom locations

              bed bedtable
              wardrobe desk laundry_basket
              bedroom_cabinet - Location
              bedside_lamp  bedroom_lamp - Lamp
              bedroom_floor - Floor
              bedroom_lightswitch 
              bedside_lamp_lightswitch - Lightswitch
               
              ; Bedroom objects
              chair small_chair
              laundry1 laundry2 laundry3 - MovableObject
              lightbulb8 lightbulb9 - Lightbulb

              ; ***************************

              ; Livingroom locations 
              couch 
              bookshelf liro_table - Location
              liro_window1 liro_window2
              liro_window3 liro_window4
              liro_window5 liro_window6 - Window
              liro_lamp couchlamp - Lamp
              liro_lightswitch 
              liro_lightswitch_cl - Lightswitch
              liro_floor - Floor

              ; Livingroom facts
              chair1 chair2 chair3
              chair4 book1 book2 - MovableObject
              lightbulb6 lightbulb10 - Lightbulb

              ; ***************************

              ; Rooms, Doors & Passes 
              corridor kitchen closet 
              bathroom wc bedroom livingroom - Room

              pass_ki_co door_be_co door_li_co
              door_cl_co door_ba_co door_wc_co
              door_out - Door
   )
  
   (:init  
    [[KNOWLEDGE BASE]]
   )

   (:goal (and 
    [[GOAL BASE]]
   )
   )
)
