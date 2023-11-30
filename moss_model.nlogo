globals [
  gas-prices
  oil-prices
  traditional-heating-system-prices
  cop  ; Coefficient of performance for heat pumps
  installation-capacity
  hassle-factor
  discount-factor
  ; Add other relevant global variables if needed
  system-cost
  scale-parameter
  gas-boiler-price
  oil-boiler-price
  electric-boiler-price
  solid-heater-price
  ASHP
  GSHP
]

breed [households household]

households-own [
  heating-system-type
  heating-system-age
  awareness-of-heat-pumps
  heating-budget
  renovation-budget
  property-value
  wants-renovation
  heating-system-broken
  relevant-heating-systems
  total-perceived-costs
  heating-system-chosen
  update-insulation
  update-heating-system
  heating-system-age
  heat-pumpsuitability
]

to setup

  clear-all
  set installation-capacity 100  ; Number of systems that can be installed per year
  set discount-factor 0.1  ; 10% discount on heat pumps
  set scale-parameter 15
  set solid-heater-price 3250
  set oil-boiler-price 3650
  set electric-boiler-price 2650
  set ASHP 10000
  set GSHP 15000


  create-households 7163 [
    setxy random-xcor random-ycor
    set shape "house"
    set heating-system-type "electric"
    set heating-system-age random 15
    set heating-budget 1000 + random 1500
    set renovation-budget 5000
    set property-value 250000
    set wants-renovation (random-float 1 < 0.1)
    set heating-system-broken false
    set update-insulation 0
    set update-heating-system 0
    ifelse random-float 1 < 0.2 [
      set heat-pumpsuitability false
    ] [
      set heat-pumpsuitability true
    ]
    ifelse random-float 1 > 0.25 [
      set awareness-of-heat-pumps false
    ] [
      set awareness-of-heat-pumps true
    ]
    set color blue
  ]

  create-households 2566 [
    setxy random-xcor random-ycor
    set shape "house"
    set heating-system-type "oil"
    set heating-system-age random 15
    set heating-budget 1000 + random 1500
    set renovation-budget 5000
    set property-value 250000
    set wants-renovation (random-float 1 < 0.1)
    set heating-system-broken false
    set update-insulation 0
    set update-heating-system 0
    ifelse random-float 1 < 0.2 [
      set heat-pumpsuitability false
    ] [
      set heat-pumpsuitability true
    ]
    ifelse random-float 1 > 0.25 [
      set awareness-of-heat-pumps false
    ] [
      set awareness-of-heat-pumps true
    ]
    set color blue
  ]

  create-households 535 [
    setxy random-xcor random-ycor
    set shape "house"
    set heating-system-type "solid"
    set heating-system-age random 15
    set heating-budget 1000 + random 1500
    set renovation-budget 5000
    set property-value 250000
    set wants-renovation (random-float 1 < 0.1)
    set heating-system-broken false
    set update-insulation 0
    set update-heating-system 0
    ifelse random-float 1 < 0.2 [
      set heat-pumpsuitability false
    ] [
      set heat-pumpsuitability true
    ]
    ifelse random-float 1 > 0.25 [
      set awareness-of-heat-pumps false
    ] [
      set awareness-of-heat-pumps true
    ]
    set color blue
  ]

  create-households 214 [
    setxy random-xcor random-ycor
    set shape "house"
    set heating-system-type "GSHP"
    set heating-system-age random 15
    set heating-budget 1000 + random 1500
    set renovation-budget 5000
    set property-value 250000
    set wants-renovation (random-float 1 < 0.1)
    set heating-system-broken false
    set update-insulation 0
    set update-heating-system 0
    ifelse random-float 1 < 0.2 [
      set heat-pumpsuitability false
    ] [
      set heat-pumpsuitability true
    ]
    ifelse random-float 1 > 0.25 [
      set awareness-of-heat-pumps false
    ] [
      set awareness-of-heat-pumps true
    ]
    set color blue
  ]

  create-households 214 [
    setxy random-xcor random-ycor
    set shape "house"
    set heating-system-type "ASHP"
    set heating-system-age random 15
    set heating-budget 1000 + random 1500
    set renovation-budget 5000
    set property-value 250000
    set wants-renovation (random-float 1 < 0.1)
    set heating-system-broken false
    set update-insulation 0
    set update-heating-system 0
    ifelse random-float 1 < 0.2 [
      set heat-pumpsuitability false
    ] [
      set heat-pumpsuitability true
    ]
    ifelse random-float 1 > 0.25 [
      set awareness-of-heat-pumps false
    ] [
      set awareness-of-heat-pumps true
    ]
    set color blue
  ]

  reset-ticks
end

to go
  ; Your go code here
end


