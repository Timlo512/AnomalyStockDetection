# AnomalyStockDetection
Anomaly Stock Detection is a project to analyze the portfolio of shareholder for each stock. It aims to cluster and detect whether some stock are anomaly from the main stream 

# Software Requirement
python=3.6.7 <br>
OS=Linux/macOS/Windows

## Installtion
Install the required packages and dependencies
```
pip install -r requirements.txt
```

To create a virtual environment, please refer to the following site:
https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/

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

the program will print the predicted anomaly stock code on the **stdout**

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Contributors
[Timothy](https://github.com/Timlo512) <br>
[Clifford](https://github.com/cliffordman) <br>
[yaqicai101](https://github.com/yaqicai101) <br>
SuJunjie <br>
Cyrus <br>

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Reference
- Alvida Mustika Rukmi et al 2019 J. Phys.: Conf. Ser. 1218 012053,Role of clustering based on density to detect patterns of stock trading deviation, Retrieved from:https://iopscience.iop.org/article/10.1088/1742-6596/1218/1/012053/pdf
- Fei Tony Liu and Kai Ming Ting, Isolation-based Anomaly Detection, Gippsland School of Information Technology, Monash University,​Retrieved from: https://cs.nju.edu.cn/zhouzh/zhouzh.files/publication/tkdd11.pdf
- Martin Ester, Hans-Peter Kriegel, Jiirg Sander, Xiaowei Xu., A Density-Based Algorithmfor Discovering Clusters in Large Spatial Databaseswith Noise, Institute for ComputerScience, University of Munich Oettingenstr. 67, D-80538Miinchen, Germany,​Retrieved from: https://www.aaai.org/Papers/KDD/1996/KDD96-037.pdf
- Maaten, Laurens van der, and Geoffrey Hinton. "Visualizing data using t-SNE." Journal of machine learning research 9.Nov (2008): 2579-2605.

