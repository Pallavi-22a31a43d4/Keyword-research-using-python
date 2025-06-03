import pandas as pd
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, StringVar, Text, Scrollbar
from IPython.display import display, clear_output

# Set up pytrends
trends = TrendReq(hl='en-US', tz=360)

def get_interest_by_region():
    s = keyword_entry.get()
    trends.build_payload(kw_list=[s])
    data = trends.interest_by_region()
    clear_output(wait=True)
    result_text.delete(1.0, "end")
    result_text.insert("end", f"{data.sample(10)}\n")

    # Plot the interest in the specified keyword by region
    df = data.sample(15)
    df.reset_index().plot(x="geoName", y=s, figsize=(12, 6), kind="bar", legend=False)
    plt.title(f'Interest in {s} by Region')
    plt.ylabel('Interest Score')
    plt.xlabel('Region')
    plt.show()

def get_trending_searches():
    m = country_entry.get()
    data = trends.trending_searches(pn=m)
    clear_output(wait=True)
    result_text.delete(1.0, "end")
    result_text.insert("end", f"{data.head(10)}\n")

def get_keyword_suggestions():
    n = suggestion_entry.get()
    keyword = trends.suggestions(keyword=n)
    data = pd.DataFrame(keyword)
    clear_output(wait=True)
    result_text.delete(1.0, "end")
    result_text.insert("end", f"{data.head()}\n")

# Create the GUI window
window = Tk()
window.title("Google Trends Analysis")

# Entry widgets for user input
keyword_label = Label(window, text="Enter a keyword for interest by region:")
keyword_entry = Entry(window)
country_label = Label(window, text="Enter a country code for trending searches (e.g., 'IN' for India):")
country_entry = Entry(window)
suggestion_label = Label(window, text="Enter a keyword for suggestions:")
suggestion_entry = Entry(window)

# Button to trigger actions
interest_button = Button(window, text="Get Interest by Region", command=get_interest_by_region)
trending_button = Button(window, text="Get Trending Searches", command=get_trending_searches)
suggestions_button = Button(window, text="Get Keyword Suggestions", command=get_keyword_suggestions)

# Text widget to display results
result_text = Text(window, height=20, width=80, wrap="word")
result_text_scrollbar = Scrollbar(window, command=result_text.yview)
result_text.config(yscrollcommand=result_text_scrollbar.set)

# Place widgets in the window
keyword_label.pack()
keyword_entry.pack()
interest_button.pack()

country_label.pack()
country_entry.pack()
trending_button.pack()

suggestion_label.pack()
suggestion_entry.pack()
suggestions_button.pack()

result_text.pack()
result_text_scrollbar.pack(side="right", fill="y")

# Start the GUI event loop
window.mainloop()
