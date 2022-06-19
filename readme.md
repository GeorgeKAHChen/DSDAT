# Dynamic System Data Analysis Tools (DSDAT)

This project combined some basic tools of stochastic dynamic system analysis, include 

## 1-d Map(D/S)

#### Data Generation

#### Lyapunov Exponent

#### Crobweb Image

## n-d Map(D/S)

#### Data Generation

#### Lyapunov Spectrum

## 1/2/3/4-d Continuous(D/S)

#### Data Generation

#### Lyapunov Spectrum

#### System Image

#### Poincare Section

## n-d Continuous(D/S)

#### Data Generation

#### Lyapunov Spectrum

## Other Functions

#### Data IO

#### Data Reduce

#### Bifucation diagram


Input Data Type     | 1-d M | n-d M | 1/2/3/4-d C | n-d C | Others | Output Data Type| memo 
---                 | ---   | ---   | ---         | ---   | ---    | --- | ---
Data Generation     | ○     | ○     | ○           | ○     |        | STD_D| SP
Stochastic System   | ○     | ○     | ○           | ○     |        | STD_D| SP
Generation with LE  | ○     | ○     | ○           | ○     |        | STD_D_LE| SP
Para - LE/LS        | ○     | ○     | ○           | ○     |        | LE_D| GPU/MP
System Image        |       |       | ○           |       |        | (Image)| SP
Crobweb Image       | ○     |       |             |       |        | (Image)| SP
Poincare Section    |       |       | ○           |       |        | STD_D(1-d M)| SP
BD Generation       | ○     | ○     | ○           | ○     |        | L_STD_D| GPU/MP
Bifucation Diagram  |       |       |             |       | ○      | (Image)| SP
Data IO             | ○     | ○     | ○           | ○     |        | | SP
Data Reduce         |       |       | ○           | ○     |        | Input| SP

* M: Map

* C: Continuous system

* SP: single processing

* GPU/MP: using gpu or multiprocessing to calculation


## Data Type Introduction

#### Standard Data Information json File
``` json
{
    "data_type": "",                        //STD_D, STD_D_LE, LE_D, L_STD_D
    "system_type": "",                      //MD, MS, CD, CS
    "data_file_name": "",
    "system_name": "",

    "t_mark": "",                           // Time parameters
    "t_save": "",
    "t_max": "",
    "delta_t": "",
    "print_delta_t": "",

    "dim": 0,                           // System dimension
    "para": 0,
    "rand": 0,
    "rand_para": 0,
    
    "para_change_loc": 0,
    "system_para": [0.0, ],             //Single group data     
    "system_para_min": [0.0, ],         // Parameters
    "system_para_max": [0.0, ],
    "system_group": [0, ],

    "axis_name":[],                         // Axis name for image plot
    "LE": "",
    "memo": ""
}
```


#### STD_D/STD_D_LE/STD_D_LEE
```
[t, Data, (LE)]
```

#### LE_D
``` 
[parameter, LE]
```


#### L_STD_D
``` 
[parameter, Data]           //time t order
```