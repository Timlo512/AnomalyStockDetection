# AnomalyStockDetection
Anomaly Stock Detection is a project to analyze the portfolio of shareholder for each stock. It aims to cluster and detect whether some stock are isolated from the main stream 

## Installtion
Install the required packages and dependencies
```
pip install -r requirements.txt
```

## Jupyter Notebook
To open Jupyter Notebook in **DataAnalysis**, execute the following code in terminal(Mac or Linux)/ Anaconda Prompt(Windows):

```
jupyter notebook --NotebookApp.iopub_data_rate_limit=1e10
```

then open **AnomalyStockDetection-Demo.ipynb** under **DataAnalysis**. 
Please ensure **utils.py** is presented in **DataAnalysis**

To install Anaconda, please download the installer at the following site:
https://www.anaconda.com/products/individual

## Usage
To run the prediction, move to the root directory of the folder, then execute the following code:

```
python main.py
```

the program will write the predicted anomaly stock code in the **prediction.log** file

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Contributors
[Timothy](https://github.com/Timlo512)

## License
[MIT](https://choosealicense.com/licenses/mit/)



