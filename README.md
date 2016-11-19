# flight combinations

https://gist.github.com/martin-kokos/7fb98650c66bd8d93767da6627affffa

## human readable output

```bash
$ cat input.csv | python3 find_combinations.py
Source: DPS 2017-02-11 01:20
Destination USM 2017-02-11 08:25
Duration: 7h 5m
Bags allowed: 1
Price: bags:0,price:96. bags:1,price:151. 
Number of flights: 2
  Flight 1: PV519: DPS 2017-02-11 01:20 ->  HKT 2017-02-11 05:00
  Delay between flights: 2h 30m
  Flight 2: PV442: HKT 2017-02-11 07:30 ->  USM 2017-02-11 08:25

...
```

## json output

```bash
$ cat input.csv | python3 find_combinations.py --json
[
    {
      "bags_allowed": 1,
      "departure": 1486895700,
      "full_price": [
          {
              "price": 159,
              "bags_count": 0
          },
          {
              "price": 227,
              "bags_count": 1
          }
      ],
      "destination": "USM",
      "arrival": 1486940400,
      "duration": 44700,
      "flights": [
          {
              "bag_price": 25,
              "bags_allowed": 1,
              "departure": 1486895700,
              "price": 50,
              "destination": "DPS",
              "arrival": 1486904100,
              "flight_number": "PV046",
              "source": "BWN"
          },
          {
              "bag_price": 38,
              "bags_allowed": 1,
              "departure": 1486912800,
              "price": 85,
              "destination": "HKT",
              "arrival": 1486926000,
              "flight_number": "PV974",
              "source": "DPS"
          },
          {
              "bag_price": 5,
              "bags_allowed": 2,
              "departure": 1486937100,
              "price": 24,
              "destination": "USM",
              "arrival": 1486940400,
              "flight_number": "PV672",
              "source": "HKT"
          }
      ],
      "source": "BWN"
  }

  ...
]
```

##  summary output

```bash
$ cat input.csv | python3 find_combinations.py --summary
BWN -> DPS. DPS -> HKT. 
BWN -> DPS. DPS -> HKT. HKT -> USM. 
DPS -> HKT. HKT -> USM. 
BWN -> DPS. DPS -> HKT. 
BWN -> DPS. DPS -> HKT. HKT -> USM. 
DPS -> HKT. HKT -> USM. 
DPS -> HKT. HKT -> USM. 
DPS -> HKT. HKT -> USM. 
DPS -> HKT. HKT -> USM. 
DPS -> HKT. HKT -> USM. 
BWN -> DPS. DPS -> HKT. 
BWN -> DPS. DPS -> HKT. HKT -> USM.

... 
```