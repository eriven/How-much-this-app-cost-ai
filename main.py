import streamlit as st
from utils.url_validator import validate_url
from utils.website_analyzer import analyze_website
from utils.cost_calculator import calculate_costs
import time

def main():
    st.set_page_config(
        page_title="Website Cost Estimator",
        page_icon="💰",
        layout="wide"
    )

    st.title("Website Cost Estimator")
    st.write("Enter a website URL to get development and maintenance cost estimates")

    # URL input
    url = st.text_input("Website URL", placeholder="https://example.com")

    if url:
        if not validate_url(url):
            st.error("Please enter a valid URL including http:// or https://")
            return

        with st.spinner("Analyzing website..."):
            try:
                # Analyze website
                complexity_metrics = analyze_website(url)
                
                # Calculate costs
                costs = calculate_costs(complexity_metrics)

                # Display results
                st.success("Analysis complete!")
                
                # Create three columns for different cost aspects
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Development Cost", f"${costs['development']:,.2f}")
                    st.write("**Breakdown:**")
                    st.write(f"- Frontend: ${costs['frontend']:,.2f}")
                    st.write(f"- Backend: ${costs['backend']:,.2f}")
                
                with col2:
                    st.metric("Monthly Hosting Cost", f"${costs['hosting']:,.2f}")
                    st.write("**Includes:**")
                    st.write("- Server costs")
                    st.write("- CDN services")
                    st.write("- SSL certificates")
                
                with col3:
                    st.metric("Monthly Maintenance", f"${costs['maintenance']:,.2f}")
                    st.write("**Includes:**")
                    st.write("- Bug fixes")
                    st.write("- Updates")
                    st.write("- Security patches")

                # Display complexity metrics
                st.subheader("Website Complexity Analysis")
                st.json(complexity_metrics)

            except Exception as e:
                st.error(f"Error analyzing website: {str(e)}")

    # Add footer
    st.markdown("---")
    st.markdown("*Note: Estimates are approximate and may vary based on specific requirements*")

if __name__ == "__main__":
    main()
