import streamlit as st 
import requests

def quran():
    response = requests.get('https://api.alquran.cloud/v1/surah')
    surahs = []
    if response.status_code == 200:
        surah_list = response.json()["data"]
        for surah in surah_list:
            surahs.append(surah["name"])
    selected_surah = st.selectbox("Select Surah",surahs)
    index = surahs.index(selected_surah)
    
    tab_arabictranslation, tab_arabic, tab_translation,  tab_audio = st.tabs([ "Arabic & Translation" ,"Arabic", "Translation", "Audio"])

    with tab_arabic:
        arabic_response = requests.get(f'https://api.alquran.cloud/v1/surah/{index+1}')
        if arabic_response.status_code == 200:
            arabic = arabic_response.json()["data"]
            st.markdown("---")
            st.subheader(arabic["name"])
            st.markdown("---")
            st.caption("Surah Number :")
            st.caption(arabic["number"])
            st.markdown("---")
            st.caption("Total Ayahs :")
            st.caption(arabic["numberOfAyahs"])
            st.markdown("---")
            ayahs = arabic["ayahs"]
            for ayah in ayahs:
                st.subheader(ayah["text"])
                st.caption(ayah["numberInSurah"])

    with tab_translation:
        translational_response = requests.get(f'https://api.alquran.cloud/v1/surah/{index+1}/en.asad')
        if translational_response.status_code == 200:
            translation = translational_response.json()["data"]
            st.markdown("---")
            st.subheader(translation["name"])
            st.markdown("---")
            st.caption("Surah Number :")
            st.caption(translation["number"])
            st.markdown("---")
            st.caption("Total Ayahs :")
            st.caption(translation["numberOfAyahs"])
            st.markdown("---")
            translations = translation["ayahs"]
            for translation_linewise in translations:
                st.subheader(translation_linewise["text"])
                st.caption(translation_linewise["numberInSurah"])

    with tab_arabictranslation:
        st.markdown("---")
        st.subheader(translation["name"])
        st.markdown("---")
        st.caption("Surah Number :")
        st.caption(translation["number"])
        st.markdown("---")
        st.caption("Total Ayahs :")
        st.caption(translation["numberOfAyahs"])
        st.markdown("---")
        translations = translation["ayahs"]
        for ayah, translation_linewise in zip(ayahs, translations):              
            st.subheader(ayah["text"])
            st.caption(translation_linewise["text"])
            st.caption(translation_linewise["numberInSurah"])
        

    with tab_audio:
        audio_response = requests.get(f'https://api.alquran.cloud/v1/surah/{index+1}/ar.alafasy')
        if audio_response.status_code == 200:
            audios = audio_response.json()["data"]
            st.markdown("---")
            st.subheader(translation["name"])
            st.markdown("---")
            st.caption("Surah Number :")
            st.caption(translation["number"])
            st.markdown("---")
            st.caption("Total Ayahs :")
            st.caption(translation["numberOfAyahs"])
            st.markdown("---")
            quran_audio = audios["ayahs"]
            for audio in quran_audio:
                st.audio(audio["audio"], format='audio/mp3')
                st.caption(audio["numberInSurah"])

    
def hadees():
    hadees_books_response = requests.get('https://hadithapi.com/api/books?apiKey=$2y$10$J8hlLbtbHrE4Efz1jAK7suw1o5EweOD3bAyXWz0rAbwQGaQfuZGpS')
    hadees_books = []
    book_slug = []
    if hadees_books_response.status_code == 200:
        hadees_books_list = hadees_books_response.json()["books"]
        for hadees_book in hadees_books_list:
            hadees_books.append(hadees_book["bookName"])
            book_slug.append(hadees_book["bookSlug"])
    selected_book = st.selectbox("Select Hadees Book",hadees_books)
    index = hadees_books.index(selected_book)
    book_Slug = book_slug[index]

    chapters_response = requests.get(f'https://hadithapi.com/api/{book_Slug}/chapters?apiKey=$2y$10$J8hlLbtbHrE4Efz1jAK7suw1o5EweOD3bAyXWz0rAbwQGaQfuZGpS')
    chapters =[]
    chapter_slugs = []
    if chapters_response.status_code == 200:
        chapters_list = chapters_response.json()["chapters"]
        for chapter_name in chapters_list:
            chapters.append(chapter_name["chapterUrdu"])
            chapter_slugs.append(chapter_name["chapterNumber"]) 

    selected_chapter = st.selectbox("Select Chapter", chapters)
    ch_idx = chapters.index(selected_chapter) 
    chapter_number = chapter_slugs[ch_idx] 


    hadith_resp = requests.get(f"https://hadithapi.com/public/api/hadiths?apiKey=$2y$10$J8hlLbtbHrE4Efz1jAK7suw1o5EweOD3bAyXWz0rAbwQGaQfuZGpS&book={book_Slug}&chapter={chapter_number}")

    if hadith_resp.status_code == 200:
        hadith_list = hadith_resp.json()["hadiths"]["data"]
        for h in hadith_list:
            st.markdown("---")
            st.caption(h["englishNarrator"])
            st.text(h["hadithUrdu"])
            st.caption(h["hadithEnglish"])
            st.caption("chapterId: " )
            st.caption(h["chapterId"])
            st.caption("Volume: " )
            st.caption(h["volume"])
            st.caption("Status: ")
            st.caption(h["status"])

def prayers_time():
    city = st.text_input("Enter your city Name: ")
    if city:
        prayer_time_response = requests.get(f'https://muslimsalat.com/{city}/weekly.json?key=e3c7be7c1146f733f6f1cdcb20d53125')
        if prayer_time_response.status_code == 200:
            prayers_timing = prayer_time_response.json().get("items", [])
            st.write("Weekly prayer times:")
            st.json(prayers_timing)
        else:
            st.error("Please check the city name.")
    else:
        st.write("Please enter the city name.")
        
 


def main():
    st.set_page_config(page_title="Hidayah-Way", layout='centered')

    st.markdown(
        """
        <style>
        h3, pre {
            line-height: 1.5 !important;  /* adjust spacing between lines */
        }
        </style>


        """,
        unsafe_allow_html=True
    )

    st.title("Hidayah-Way")
    st.subheader("Your path to Quran, Sunnah & Salah times.")

    menu = st.sidebar.selectbox("Selction",["Quran","Hadees", "Prayers Time"])

    if menu == "Quran":
       quran()

    elif menu == "Hadees":
        hadees()

    elif menu == "Prayers Time":
        prayers_time()
        

if __name__ == main():
    main()



