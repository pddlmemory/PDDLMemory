(define (domain appartment)
  
   (:requirements :strips :typing)
   
   (:types Location MovableObject Person Room - Object
           Window Floor Door Lightswitch Lamp - Location
           Lightbulb CleaningProducts - MovableObject
   )

   (:predicates (own-location ?l - Location)                    ; Own Location
                (is-at ?l - Location ?o - Object)               ; Location of an Object
                (is-in ?r - Room ?l - Location)                 ; Location is in Room
                (is-dirty-loc ?l - Location)                    ; Location is dirty
                (is-dirty-mobj ?mo - MovableObject)             ; MovableObject is dirty
                (is-attached ?mo - MovableObject)               ; Object is attached / is not movable
                (is-intact ?lb - Lightbulb)                     ; Lightbulb is intact
                (is-working ?l - Lamp)                          ; Lamp is working
   )
   
   (:action go
       :parameters (?from ?to - Location ?r - Room)
       :precondition (and (own-location ?from)
                          (is-in ?r ?from)
                          (is-in ?r ?to)
                      )
       :effect (and (not (own-location ?from))
                    (own-location ?to)
                )
   )

   (:action move
       :parameters (?mo - MovableObject ?from ?to - Location ?r - Room)
       :precondition (and (own-location ?from)
                          (is-at ?from ?mo)
                          (not (is-attached ?mo))
                          (is-in ?r ?from)
                          (is-in ?r ?to)
                      )
       :effect (and (not (own-location ?from))
                    (not (is-at ?from ?mo))
                    (own-location ?to)
                    (is-at ?to ?mo)
                )
   )

   (:action clean
      :parameters (?l - Location ?cp - CleaningProducts)
      :precondition (and (own-location ?l)
                         (is-dirty-loc ?l)
                         (is-at ?l ?cp)
                     )
      :effect (not (is-dirty-loc ?l))
    )

    (:action change-lightbulb
      :parameters (?l - Lamp ?lb1 ?lb2 - Lightbulb)
      :precondition (and 
                         (own-location ?l)
                         (not (is-working ?l))
                         (not (= ?lb1 ?lb2))
                         (is-attached ?lb1)
                         (is-at ?l ?lb1)
                         (is-at ?l ?lb2)
                    )
      :effect (and 
                        (not (is-attached ?lb1))
                        (is-attached ?lb2)
                        (is-working ?l)
              )
    )




)
