import streamlit as st

def display_project_scope_justification():
    scope = {
        "Product Categories and Strategic Importance": [
            {
                "HS Code": 84,
                "Category": "Machinery & Mechanical Appliances",
                "Justification": (
                    "Subject to significant U.S. tariffs, this category underpins global industrial manufacturing. "
                    "It plays a critical role in factory automation, production equipment, and capital goods, making it essential "
                    "for both exporting and importing economies."
                ),
            },
            {
                "HS Code": 85,
                "Category": "Electrical Machinery & Equipment",
                "Justification": (
                    "Encompassing semiconductors, circuits, and telecom hardware, this category is pivotal in the global technology "
                    "supply chain. Strategic due to its impact on national security, digital infrastructure, and innovation competitiveness."
                ),
            },
            {
                "HS Code": 94,
                "Category": "Furniture",
                "Justification": (
                    "A key Chinese export category severely affected by U.S. tariffs, disrupting supply chains for retailers and "
                    "manufacturers globally. Its inclusion illustrates the broader impact."
                ),
            },
            {
                "HS Code": 12,
                "Category": "Oil Seeds",
                "Justification": (
                    "Soybeans are central to China's retaliatory measures against U.S. agriculture, impacting agricultural trade dynamics."
                ),
            },
            {
                "HS Code": 39,
                "Category": "Plastics & Plastic Products",
                "Justification": (
                    "Widely used across industries and affected by tariffs in both directions, making it significant for multiple sectors."
                ),
            },
            {
                "HS Code": 87,
                "Category": "Vehicles & Automotive Parts",
                "Justification": (
                    "Targeted by both the U.S. and China, this category is critical for global automotive manufacturing and supply chain continuity."
                ),
            },
            {
                "HS Code": 90,
                "Category": "Optical, Medical & Precision Instruments",
                "Justification": (
                    "U.S. concerns over Chinese tech development lead to tariffs on high-end equipment, highlighting the intersection of trade and technology policy."
                ),
            },
        ],
        "Countries Involved": [
            "China",
            "U.S.",
            "Malaysia",
            "Vietnam",
            "South Korea",
            "Germany",
            "Canada"
        ]
    }

    st.markdown(
        "- Trade data was obtained from the [International Trade Map](https://www.trademap.org/Index.aspx). "
        "Initially, the dataset included trade flows with **all countries**.\n"
        "- We performed data cleaning to **filter out irrelevant countries** and **focused only on the 7 target countries**.\n"
        "- Trade balances were then analyzed across **7 HS code product categories**, allowing us to explore strategic trade trends and impacts of global tariff policies."
    )

    st.subheader("Project Scope and Justification")

    st.markdown("#### Product Categories and Strategic Importance")
    for item in scope["Product Categories and Strategic Importance"]:
        st.markdown(f"**HS Code {item['HS Code']} – {item['Category']}**")
        st.markdown(f"- {item['Justification']}")

    st.markdown("#### Countries Involved")
    st.write(", ".join(scope["Countries Involved"]))

    st.markdown("#### Country Selection Justification")
    justifications = {
        "China": "Central player in the trade war and global manufacturing hub. Directly targeted by U.S. tariffs on electronics, machinery, and furniture.",
        "U.S.": "Initiator of tariff measures; impacted by retaliatory tariffs, especially in agriculture and automotive sectors.",
        "Malaysia": "Part of the regional supply chain for electronics/machinery. Benefited from trade diversion as production shifts from China.",
        "Vietnam": "Major relocation destination for manufacturers avoiding China tariffs. Rapid export growth to the U.S.",
        "South Korea": "Key technology exporter, especially semiconductors and electronics. Vulnerable to trade disruptions in high-tech goods.",
        "Germany": "Europe's top exporter of machinery and vehicles. Sensitive to changes in global trade demand and policy uncertainty.",
        "Canada": "Major U.S. trade partner; affected via agricultural and resource trade, as well as supply chain interdependence."
    }

    for country, reason in justifications.items():
        st.markdown(f"**{country}**: {reason}")
