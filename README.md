# Portfolio Project: Brain Cancer classification using a hybrid quantum Classical model <🧠|1>

Brain Tunor Detection is a development of a website linked to a quantum network. The goal of our project is to eventually deploy on our server a link with a neuronal network developed that helps it to detect the major types of tumor, analyzed and provide it with the result. 

## Functionalities of this application:
* Retrieve patient X-ray image
* Analyze the image and do some operations on it
* predict the result and display it
* Update the database 

## Table of Content
* [Environment](#environment)
* [Installation](#installation)
* [Technology](#Technology)
* [library](#library)
* [Architecture](#architecture)
* [Bugs](#bugs)
* [Authors](#authors)
* [License](#license)

## Environment
This project is interpreted/tested on Ubuntu 14.04 LTS using python3 (version 3.4.3)


## Installation
* Clone this repository: `git clone "https://github.com/ggirlk/Brain_Cancer_Classification.git"`
* Access deployment directory: `cd deployment`
* Run the command: `python manage.py runserver`
* Browse your X-ray  and wait for the result

## Technology

* Quantum computing
Our project we chose to work with quantum computing, a new but efficient technology, with a high precision rate.
Quantum computing, uses quantum bits or qubits. It harnesses the unique ability of subatomic particles which allows them to 
exist in more than one state ( 1 and a 0 at the same time).
<p>qbits:</p>
The basic unit of information in quantum computing.which represents the state of a quantum particle. Because of superposition, qubits can either be 1 or 0 or anything in between.
<p>Gates:</p>
a quantum gate is a basic quantum circuit operating on a number of qubits. They are the building blocks of quantum circuits.

* Python / Django
Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design


## library
- Qiskit:
 is an open-source software development kit  SDK for working with quantum computers
- pennylane 
PennyLane is a cross-platform Python library for quantum machine learning
-  Tensorflow
TensorFlow is an end-to-end open source platform for machine learning.
- datetime 
module supplies classes for manipulating dates and times.
- h5py
package  to store huge amounts of numerical data, and easily manipulate that data from NumPy
- cv2(openCv)

## architecture
![plot](./architecture.png)

## Bugs
No known bugs at this time. 

## Authors
- Mouhamed charfi - [Github](https://github.com/medcharfi96) / [Twitter](https://twitter.com/mouhamedcharfi)
- Ghofrane laabidi - [Github](https://github.com/anaruzz) / [Twitter](https://twitter.com/)
- Khouloud khammesi - [Github](https://github.com/ggirlk) / [Twitter](https://twitter.com/)


## License
Public Domain. No copy write protection. 


