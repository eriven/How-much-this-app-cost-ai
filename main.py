import streamlit as st
from utils.url_validator import validate_url
from utils.website_analyzer import analyze_website
from utils.cost_calculator import calculate_costs
import time


def format_size(size_bytes):
    """Format content length to human readable size"""
    for unit in ['chars', 'K chars', 'M chars']:
        if size_bytes < 1000:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1000
    return f"{size_bytes:.1f} G chars"


def main():
    st.set_page_config(page_title="How much this app cost",
                       page_icon="💰",
                       layout="wide")

    st.title("How much this app cost")
    st.write(
        "Enter a website URL to get development and maintenance cost estimates"
    )

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
                    st.metric("Development Cost",
                              f"${costs['development']:,.2f}")
                    st.write("**Breakdown:**")
                    st.write(f"- Frontend: ${costs['frontend']:,.2f}")
                    st.write(f"- Backend: ${costs['backend']:,.2f}")

                with col2:
                    st.metric("Monthly Hosting Cost",
                              f"${costs['hosting']:,.2f}")
                    st.write("**Includes:**")
                    st.write("- Server costs")
                    st.write("- CDN services")
                    st.write("- SSL certificates")

                with col3:
                    st.metric("Monthly Maintenance",
                              f"${costs['maintenance']:,.2f}")
                    st.write("**Includes:**")
                    st.write("- Bug fixes")
                    st.write("- Updates")
                    st.write("- Security patches")

                # Display complexity metrics with improved UI
                st.subheader("Website Complexity Analysis")

                # Overall complexity score with progress bar
                st.write("### Overall Complexity")
                complexity_score = complexity_metrics['complexity_score']
                st.progress(complexity_score / 10)
                st.metric("Complexity Score", f"{complexity_score:.1f}/10")

                # Create two columns for metrics
                metrics_col1, metrics_col2 = st.columns(2)

                with metrics_col1:
                    st.write("### Size Metrics")
                    st.metric(
                        "Content Size",
                        format_size(complexity_metrics['content_length']),
                        help="Total amount of content found on the website")
                    st.metric(
                        "Estimated Pages",
                        complexity_metrics['estimated_pages'],
                        help="Approximate number of pages the website contains"
                    )

                with metrics_col2:
                    st.write("### Feature Detection")
                    # Create a card-like container for features
                    with st.container():
                        features_data = {
                            "Forms":
                            complexity_metrics['has_forms'],
                            "Authentication":
                            complexity_metrics['has_authentication'],
                            "Dynamic Content":
                            complexity_metrics['has_dynamic_content']
                        }

                        for feature, has_feature in features_data.items():
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.write(f"**{feature}:**")
                            with col2:
                                if has_feature:
                                    st.success("Yes")
                                else:
                                    st.error("No")

            except Exception as e:
                st.error(f"Error analyzing website: {str(e)}")

    # Add footer
    st.markdown("---")
    st.markdown(
        "*Note: Estimates are approximate and may vary based on specific requirements*"
    )


if __name__ == "__main__":
    main()
