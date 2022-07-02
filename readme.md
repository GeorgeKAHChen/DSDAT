# Dynamic System Data Analysis Tools (DSDAT)

This project combined some basic tools of stochastic dynamic system analysis, include 

## 0 Data Generator

This tool can compute the orbit of systems and LE in the same time.

#### 01. Just Save orbit

save orbit(STD) without calculate LE

#### 10: Just Save LE

not save orbit(STD) and calculate LE

#### 11: Save both LE and orbit

save both orbit(STD) and calculate LE




## 1 Data Merge

This tool can merge data files for LE plot or bifucation diagram plot.

### flags

#### 0: Merge LE

merge LE data from json files 

#### 1: Merge Data

merge STD data to LSTD

## 2 Image Plot

This tools can plot image depend on the `data_type`, `system_type` and `dim`

### flags

#### [plot file name] flags

flags table
Input Data Type     | 1-dim | 2-dim | 3-dim | 4-dim             | n-dim
---                 | ---   | ---   | ---   | ---               | ---
STD                 | /     | /     | /     | [i,j]/[i,j,k]     | [i,j]/[i,j,k]
LE                  | /     | /     | /     | [fig1, fig2, ...] |  [fig1, fig2, ...] 
LSTD                | /     | i     | i     | i                 | i


#### `STD`: [i, j]/[i, j, k]

The system higher than 3 dimension will print 2/3-d dim figure depend on flag

#### `LSTD`: i

The system higher than 1 dimension will print bifucation diagram of parameter - x_i figure

#### `LE`: [fig1, fig2, ..., fign]

The system higher than 3 dimension will print n subfigure, every subfigure include fig_i LE.



## Poincare section

not finish

## Data Generation

#### Data Reduce

not finish



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


#### STD(.data)
``` dat
[t, x1, x2, ...]
```

#### LE(.data)
``` dat
[parameter, LE1, LE2, ...]
```

#### LSTD(.data)
``` dat
[parameter, x1, x2, ...]
```

#### code std_input array
``` python
#inputs data structure

inputs[0] = (float) curr_t;
inputs[1] = array[TensorDouble] curr_x;
inputs[2] = array[TensorDouble] dyn_para;
inputs[3] = array[TensorDouble] rand_para;
inputs[4] = array[TensorDouble] eye Gram_S(matrix);
inputs[5] = array[TensorDouble] LE;
inputs[6] = array[TensorDouble] random_value;
inputs[7] = array[TensorDouble] jacobian;
inputs[8] = array[double]: LE_table / Value table;
```



