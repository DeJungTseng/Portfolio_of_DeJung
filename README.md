# Tseng, De-Jung
## About Me
* A Neuroscrientist
* Interested in smart health product deveploing
* Familiar with data mining and UX design
  
## My Works
[Flask Webpage](https://dian-ying-tui-jian-xi-tong.onrender.com/login)
![一頁式簡報](https://github.com/user-attachments/assets/09946f21-a491-4c5a-8d18-649d68439766)


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

## 🧪 Mock Mode Support

If the app cannot connect to a PostgreSQL database, it will automatically switch to **mock mode**, where:

- Users `ddd` and `eee` can log in using passwords `DDD` and `EEE`
- Watch history and recommendations are generated from predefined mock data

This allows users to explore the interface and functionality **without setting up a database**.





