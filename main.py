import streamlit as st
import json
import requests
import pandas as pd

api_key = "AIzaSyDo1oCgpOyprr2WlprJU8xNTOVka5K_SOQ"
# https://pollen.googleapis.com/v1/forecast:lookup?key=YOUR_API_KEY


def getPlantData():
    plant_data = []
    for plant in basic_data['dailyInfo'][0]['plantInfo']:
        category = "N/A"
        index_description = "N/A"
        if 'indexInfo' in plant:
            category = plant['indexInfo'].get('category', "N/A")
            index_description = plant['indexInfo'].get('indexDescription', "N/A")
        plant_data.append({
            "displayName": plant['displayName'],
            "inSeason": plant.get('inSeason', False),
            "category": category,
            "indexDescription": index_description
        })
    return plant_data


def getnumGrass():
    numGrass = 0
    for plant in basic_data['dailyInfo'][0]['plantInfo']:
        if 'plantDescription' in plant:
            plant_type = plant['plantDescription'].get('type', 'N/A')
            if plant_type == 'GRASS':
                numGrass += 1
            else:
                continue
    return numGrass


def getGrassPlants():
    plant_data = []
    for plant in basic_data['dailyInfo'][0]['plantInfo']:
        if 'plantDescription' in plant and plant['plantDescription']['type'] == 'GRASS':
            plant_data.append({
                    "family": plant['plantDescription'].get('family', 'N/A'),
                    "seasonActive": plant['plantDescription'].get('season', 'N/A'),
                    "crossReaction": plant['plantDescription'].get('crossReaction', 'N/A'),
                    "picture": plant['plantDescription'].get('picture', 'N/A'),
                    "closeUpPicture": plant['plantDescription'].get('pictureCloseup', 'N/A')
                })
    return plant_data


def getnumTree():
    numTree = 0
    for plant in basic_data['dailyInfo'][0]['plantInfo']:
        if 'plantDescription' in plant:
            plant_type = plant['plantDescription'].get('type', 'N/A')
            if plant_type == 'TREE':
                numTree += 1
            else:
                continue
    return numTree


def getTreePlants():
    plant_data = []
    for plant in basic_data['dailyInfo'][0]['plantInfo']:
        if 'plantDescription' in plant and plant['plantDescription']['type'] == 'TREE':
            plant_data.append({
                    "family": plant['plantDescription'].get('family', 'N/A'),
                    "seasonActive": plant['plantDescription'].get('season', 'N/A'),
                    "crossReaction": plant['plantDescription'].get('crossReaction', 'N/A'),
                    "picture": plant['plantDescription'].get('picture', 'N/A'),
                    "closeUpPicture": plant['plantDescription'].get('pictureCloseup', 'N/A')
                })
    return plant_data


def getnumWeed():
    numWeed = 0
    for plant in basic_data['dailyInfo'][0]['plantInfo']:
        if 'plantDescription' in plant:
            plant_type = plant['plantDescription'].get('type', 'N/A')
            if plant_type == 'WEED':
                numWeed += 1
            else:
                continue
    return numWeed


def getWeedPlants():
    plant_data = []
    for plant in basic_data['dailyInfo'][0]['plantInfo']:
        if 'plantDescription' in plant and plant['plantDescription']['type'] == 'WEED':
            plant_data.append({
                    "family": plant['plantDescription'].get('family', 'N/A'),
                    "seasonActive": plant['plantDescription'].get('season', 'N/A'),
                    "crossReaction": plant['plantDescription'].get('crossReaction', 'N/A'),
                    "picture": plant['plantDescription'].get('picture', 'N/A'),
                    "closeUpPicture": plant['plantDescription'].get('pictureCloseup', 'N/A')
                })
    return plant_data



category = st.sidebar.selectbox("Choose a category:", ("Current Forecast Data", "Pollen Plant Descriptions", "Feedback Form"))

st.title("Pollen Web App")

if category == "Current Forecast Data" or category == "Pollen Plant Descriptions":
    st.subheader("Find the pollen forecast in your area")
    latitude = st.text_input("Enter the latitude of the location:", placeholder="ex. 32.32")
    longitude = st.text_input("Enter the longitude of the location:", placeholder="ex. 35.22")
    if st.button('Submit'):
        url = f"https://pollen.googleapis.com/v1/forecast:lookup?key={api_key}&location.longitude={longitude}&location.latitude={latitude}&days=1"
        response = requests.get(url)
        if response.status_code == 200:
            basic_data = json.loads(response.text)
            st.success("Your request was successful!")
            if category == "Current Forecast Data":
                tab1, tab2, tab3 = st.tabs(["Data Frame", "Bar Graph", "Line Graph"])
                with tab1:
                    df = pd.DataFrame(getPlantData())
                    st.dataframe(
                        df,
                        column_config={
                            "displayName": "Plant name",
                            "inSeason": "In Season?",
                            "category": "Intensity",
                            "indexDescription": "Description"
                        },
                        use_container_width=True,
                    )

                with tab2:
                    chart_data = {"Type of Pollen": ["Grass", "Tree", "Weed"],
                                  "Number of Plants": [getnumGrass(), getnumTree(), getnumWeed()]}
                    st.bar_chart(
                        chart_data, x="Type of Pollen", y="Number of Plants"
                    )

                with tab3:
                    chart_data = {"Type of Pollen": ["Grass", "Tree", "Weed"],
                                  "Number of Plants": [getnumGrass(), getnumTree(), getnumWeed()]}
                    st.line_chart(
                        chart_data, x="Type of Pollen", y="Number of Plants"
                    )

            elif category == "Pollen Plant Descriptions":
                tab1, tab2, tab3 = st.tabs(["Grass Pollens", "Tree Pollens", "Weed Pollens"])
                with tab1:
                    df = pd.DataFrame(getGrassPlants())
                    st.dataframe(
                        df,
                        column_config={
                            "family": "Plant family",
                            "seasonActive": "Seasons Active",
                            "crossReaction": "Cross Reaction Description",
                            "picture": st.column_config.LinkColumn("Picture URL"),
                            "closeUpPicture": st.column_config.LinkColumn("Close Up Picture URL")
                        },
                        use_container_width=True,
                    )

                with tab2:
                    df = pd.DataFrame(getTreePlants())
                    st.dataframe(
                        df,
                        column_config={
                            "family": "Plant family",
                            "seasonActive": "Seasons Active",
                            "crossReaction": "Cross Reaction Description",
                            "picture": st.column_config.LinkColumn("Picture URL"),
                            "closeUpPicture": st.column_config.LinkColumn("Close Up Picture URL")
                        },
                        use_container_width=True,
                    )

                with tab3:
                    df = pd.DataFrame(getWeedPlants())
                    st.dataframe(
                        df,
                        column_config={
                            "family": "Plant family",
                            "seasonActive": "Seasons Active",
                            "crossReaction": "Cross Reaction Description",
                            "picture": st.column_config.LinkColumn("Picture URL"),
                            "closeUpPicture": st.column_config.LinkColumn("Close Up Picture URL")
                        },
                        use_container_width=True,
                    )

        else:
            st.error("Error in getting forecast data. Please check your input and try again.")

    else:
        st.info("Click the Submit button to see the current forecast data")

elif category == "Feedback Form":
    st.subheader("Feedback Form")
    st.text("We would love to hear your feedback!")
    name = st.text_input("Full Name:")
    age = st.number_input("Age:")
    email = st.text_input("Email Address:")
    useful = st.radio("Was this website useful?", ("Yes", "No"), index=None)
    use_again = st.radio("Would you use this website again?", ("Yes","No"), index=None)
    feedback = st.text_area("Feedback", "")

    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")
