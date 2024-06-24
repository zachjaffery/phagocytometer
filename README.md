# Phagocytometer

This program was made to expedite counting cells after imaging. Images are taken with neutrophils stained one color and yeast stained another, then the painstaking task of counting each image is performed. With this program, you can run some code and receive a CSV of cell counts for each photo taken.

## Installation

The program relies on python, so prior to use python and the required libraries must be installed. You can find this at [python.org](python.org). The program was built in version 3.9.1, but may work on other versions.

Additionally, several packages are required. The package installer 'pip' shoudld come automatically with python, but follow instruction at [https://packaging.python.org/en/latest/tutorials/installing-packages/](https://packaging.python.org/en/latest/tutorials/installing-packages/) to ensure you have it.

Then, in the terminal (Windows Key + X -> Terminal), paste and run the following code:

>pip install numpy<br />
>pip install pandas<br />
>pip install opencv-python<br />
>pip install tk<br />
>pip install customtkinter



## Usage
Open the TIF file you want to read. NOTE: The program assumes that the order of the channels in the TIF stack are 1) blue, 2) DIC, 3) green. This is important because the channels need to be separated to be analzyed. If the TIF file has a different order, then the program in its current state will not give the desired result. 

You also may want to choose a name for the CSV file being created. If no name is given, the program will return a file name with the current date and time.

### Batch Processing

If you click on the button in the lower left corner, the batch processing dialog will open. You can select as many TIFs as you want, and the program will count them all. Currently, file name is set to "batch_1," "batch_2," etc. 


## Issues
Please direct all issues, or feature suggestions, to zachjaffery@gmail.com. I will try to help as best I can. 
