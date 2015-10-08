;; A Hacker World Problem
;;
;; Domain Author: Volker Strobel
;; Problem Author: Ivo Chichkov

(define (problem hacker-world-problem)
  (:domain hacker-world)
  (:objects

    alice bob - non-hacker
    mallory - hacker

    alice-email bob-email online-banking pizza_de - software

    mallory-fridge - fridge
    cheeseburger - burger
    pizza1 - supreme
    pizza2 - peperoni


  )
  (:init
    [[KNOWLEDGE BASE]]
  )

  (:goal
    (and
     [[GOAL BASE]]
    )
  )
)