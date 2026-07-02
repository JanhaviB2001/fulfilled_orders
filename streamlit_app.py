# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title(f":cup_with_straw: Pending Smoothie Orders :cup_with_straw:")
st.write(
  """ Orders that need to be filled.
  """
)


session = get_active_session()

my_dataframe = (
    session.table("SMOOTHIES.PUBLIC.ORDERS")
    .filter(col("ORDER_FILLED") == 0)
)

rows = my_dataframe.collect()

if rows:
    editable_df = st.data_editor(rows)

    submitted = st.button("Submit")

    if submitted:
        og_dataset = session.table("SMOOTHIES.PUBLIC.ORDERS")
        edited_dataset = session.create_dataframe(editable_df)

        try:
            og_dataset.merge(
                edited_dataset,
                og_dataset["ORDER_UID"] == edited_dataset["ORDER_UID"],
                [when_matched().update({"ORDER_FILLED": edited_dataset["ORDER_FILLED"]})]
            )
            st.success("Order(s) Updated!", icon="👍")
        except Exception as e:
            st.error(f"Something went wrong: {e}")

else:
    st.success("There are no pending orders right now.", icon="👍")
