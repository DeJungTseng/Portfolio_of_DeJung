# 🎥 Personalized Video Recommendation System

A content-based video recommendation system with a graphical interface built using `Tkinter`.

## 🔍 Features

- 🖥️ GUI built with **Tkinter** for a user-friendly experience
- 🔐 Secure **login system** for personal video platform accounts
- 📊 Loads **watch history** and recommends new content based on user behavior
- 🔑 **Password encryption** to protect user privacy and account security


## 🛠️ Tech Stack

- **Python**: Data processing, modeling
- **scikit-learn**: Model training
- **PostgreSQL**: Data storage
- **Tkinter**: User Interface
- **Pandas / NumPy / Matplotlib**: Data analysis and visualization
- **bcrypt**: Password hashing and encryption for secure login

## 📈 Project Flow

1. 🧼 **Data Preprocessing**: Clean and structure movie and user data  
2. 🧠 **Model Training**: Use Random Forest Regression on training set  
3. 📊 **Prediction**: Generate top-N movie suggestions  
4. 🖥️ **Frontend Integration**: Display results in GUI

## 🧩 Software Architecture

This system integrates a Tkinter-based GUI with a content-based video recommendation engine, incorporating secure login, user history analysis, and random forest model predictions.

![Software Architecture Diagram](./docs/software_architecture.png)


## 🖼️ Demo
- **Login**  
  ![UI Login](./docs/login.png)

- **Recommendation for User 1**  
  ![Recommendation User 1](./docs/recommend_a.jpg)

- **Recommendation for User 2**  
  ![Recommendation User 2](./docs/recommend_b.jpg) 
_Run `python mian.py` to launch the interface._

## 🚀 Getting Started

```bash
# Clone this repository
git clone https://github.com/DeJungTseng/Portfolio_of_DeJung
cd Python_Windows_TK

# Install dependencies
pip install -r requirements.txt

# Start the app
python main.py
