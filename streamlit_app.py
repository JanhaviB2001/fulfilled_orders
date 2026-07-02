import streamlit as st
from snowflake.snowpark.functions import col, when_matched

# Page title
st.title(":cup_with_straw: Pending Smoothie Orders :cup_with_straw:")
st.write("Orders that need to be filled.")

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Get pending orders
orders_df = (
    session.table("SMOOTHIES.PUBLIC.ORDERS")
    .filter(col("ORDER_FILLED") == 0)
)

rows = orders_df.collect()

if rows:

    # Editable table
    edited_df = st.data_editor(
        rows,
        use_container_width=True,
        num_rows="fixed"
    )

    if st.button("Submit"):

        original_table = session.table("SMOOTHIES.PUBLIC.ORDERS")
        updated_table = session.create_dataframe(edited_df)

        try:
            original_table.merge(
                updated_table,
                original_table["ORDER_UID"] == updated_table["ORDER_UID"],
                [
                    when_matched().update(
                        {
                            "ORDER_FILLED": updated_table["ORDER_FILLED"]
                        }
                    )
                ],
            )

            st.success("Order(s) Updated! 👍")

        except Exception as e:
            st.error(f"Something went wrong: {e}")

else:
    st.success("There are no pending orders right now. 👍")
