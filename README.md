# flight combinations

https://gist.github.com/martin-kokos/7fb98650c66bd8d93767da6627affffa

## human readable output

```bash
cat input.csv | python3 find_combinations.py
```

### example

```
Source: USM 2017-02-12 06:15:00, Destination HKT 2017-02-12 11:30:00, Duration: 5h 15m 0s. Bags allowed: 1. Price: [{'price': 56, 'bags_count': 0}, {'price': 89, 'bags_count': 1}]
PV870: USM 2017-02-12 06:15:00 ->  HKT 2017-02-12 07:15:00
diff between flights: 1h 0m 0s
PV837: HKT 2017-02-12 08:15:00 ->  USM 2017-02-12 09:10:00
diff between flights: 1h 20m 0s
PV290: USM 2017-02-12 10:30:00 ->  HKT 2017-02-12 11:30:00

```

## json output

```bash
cat input.csv | python3 find_combinations.py --json
```

### example

```json
[
  {
    "source": "BWN",
    "destination": "HKT",
    "departure": 1486780500,
    "arrival": 1486816200,
    "duration": 35700,
    "bags_allowed": 1,
    "full_price": [
      {
        "bags_count": 0,
        "price": 135
      },
      {
        "bags_count": 1,
        "price": 212
      }
    ],
    "flights": [
      {
        "flight_number": "PV873",
        "source": "BWN",
        "destination": "DPS",
        "departure": 1486780500,
        "arrival": 1486788900,
        "price": 46,
        "bags_allowed": 1,
        "bag_price": 34
      },
      {
        "flight_number": "PV260",
        "source": "DPS",
        "departure": 1486803000,
        "destination": "HKT",
        "arrival": 1486816200,
        "price": 89,
        "bags_allowed": 1,
        "bag_price": 43
      }
    ]
  }
]
```