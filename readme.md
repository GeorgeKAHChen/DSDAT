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
Data Generation     | ○     | ○     | ○           | ○     |        | STD_D| GPU/MP
Stochastic System   | ○     | ○     | ○           | ○     |        | STD_D| GPU/MP
Generation with LE  | ○     | ○     | ○           | ○     |        | STD_D_LE| GPU/MP
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
deafult.json
```json
{
    "dyn": "model.Lorenz",                  // Model name and location

    "delta_t": 1e-1,                        // delta_t for computation
    "delta_t_save": -1,                     // delta_t for save and plot
    "t_max":  100,                          // final t for computation
    "t_mark": 90,                           // t start LE iteration
    "t_save": 90,                           // t start to save

    "default_data_folder": "Local_Output",  // folder for save data
    "default_LE_folder": "tmp_LE_input",    // folder for merge data to LE
    "default_BD_folder": "tmp_BD_input",    // folder for merge data to LSTD
    "image_data_file": "",
    
    "save_image_local": 1,                  // Save image when plot
    "device": "cpu"                         // Use cpu or cuda(:1/:2)
}
```


#### Standard Data Information json File
``` json
{
    "data_type": "",                        // STD, LSTD, LE
    "system_type": "",                      // MD, MS, CD, CS
    "data_file_name": "",
    "system_name": "",

    "t_mark": "",                           // Time parameters
    "t_max": "",
    "t_save": "",
    "delta_t": "",
    "print_delta_t": "",

    "dim": 0,                               // System dimension
    "para": 0,
    "rand": 0,
    "rand_para": 0,
    
    "para_change_loc": 0,
    "system_para": [0.0, ],                 // Single group data     
    "system_para_min": [0.0, ],             // Parameters
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