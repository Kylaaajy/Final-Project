import streamlit as st
import openai
from streamlit.report_thread import async_to_sync
import asyncio

from openai import AsyncOpenAI

@@ -37,23 +37,27 @@ def app():
    if st.session_state.step == 2:
        if st.button("Get Travel Recommendation"):
            st.session_state.step = 3  # Proceed to show the recommendation
            st.experimental_rerun()
            st.rerun()

    if st.session_state.step == 3:
        if 'itinerary' not in st.session_state:
            itinerary = async_to_sync(generate_travel_recommendation)(
                st.session_state.destination,
                st.session_state.duration,
                st.session_state.interests
            )
            st.session_state.itinerary = itinerary
            async def fetch_itinerary():
                itinerary = await generate_travel_recommendation(
                    st.session_state.destination,
                    st.session_state.duration,
                    st.session_state.interests
                )
                st.session_state.itinerary = itinerary
                st.rerun()

            asyncio.run(fetch_itinerary())
        else:
            st.write(f"Recommended itinerary for your trip to {st.session_state.destination} for {st.session_state.duration} days, focusing on {st.session_state.interests}, is: {st.session_state.itinerary}")
            if st.button("Start Over"):
                for key in ['step', 'destination', 'duration', 'interests', 'itinerary']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.experimental_rerun()
                st.rerun()

if __name__ == "__main__":
    app()
