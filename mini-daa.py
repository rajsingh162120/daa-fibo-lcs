import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# Function to calculate Fibonacci sequence using bottom-up dynamic programming
def fibonacci_sequence(n):
    fib_sequence = [0, 1]
    if n <= 1:
        return fib_sequence[:n+1]
    for i in range(2, n + 1):
        fib_sequence.append(fib_sequence[i - 1] + fib_sequence[i - 2])
    return fib_sequence

# Function to calculate Fibonacci number using bottom-up dynamic programming
def fibonacci(n):
    fib = [0, 1]
    if n <= 1:
        return fib[n]
    for i in range(2, n + 1):
        fib.append(fib[i - 1] + fib[i - 2])
    return fib[n]

# Function to find Longest Common Subsequence (LCS) using bottom-up dynamic programming
def longest_common_subsequence(X, Y):
    m = len(X)
    n = len(Y)

    # Creating LCS table
    LCS_table = [[0] * (n + 1) for _ in range(m + 1)]

    # Filling the LCS table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                LCS_table[i][j] = LCS_table[i - 1][j - 1] + 1
            else:
                LCS_table[i][j] = max(LCS_table[i - 1][j], LCS_table[i][j - 1])

    return LCS_table

def display_LCS_table(X, Y):
    LCS_table = longest_common_subsequence(X, Y)

    # Convert LCS table to pandas DataFrame for easy display
    cols_X = [f"{char}_X{i+1}" for i, char in enumerate(X)]
    cols_Y = [f"{char}_Y{i+1}" for i, char in enumerate(Y)]
    df = pd.DataFrame(LCS_table, columns=[''] + cols_Y, index=[''] + cols_X)
    
    # Displaying LCS table in matrix form
    st.write("LCS Table:")
    st.table(df)

    return LCS_table


def get_LCS(X, Y, LCS_table):
    m = len(X)
    n = len(Y)
    LCS = []

    # Reconstructing LCS from the table
    while m > 0 and n > 0:
        if X[m - 1] == Y[n - 1]:
            LCS.append(X[m - 1])
            m -= 1
            n -= 1
        elif LCS_table[m - 1][n] > LCS_table[m][n - 1]:
            m -= 1
        else:
            n -= 1

    return ''.join(reversed(LCS))

def main():
    st.sidebar.title("Select an Option")
    app_selection = st.sidebar.radio("", ("Fibonacci Sequence", "Longest Common Subsequence (LCS)"))

    if app_selection == "Fibonacci Sequence":
        st.title("Fibonacci Sequence")
        # User input for Fibonacci number
        fib_input = st.number_input("Enter a number:", min_value=0, step=1)
        if st.button("Calculate Fibonacci"):
            fib_result = fibonacci(int(fib_input))
            st.write("Fibonacci of", fib_input, "is", fib_result)

        st.title("Fibonacci Sequence Slider")
        # User input for Fibonacci sequence length
        n = st.slider("Select the length of Fibonacci sequence:", min_value=2, max_value=100, value=10)

        # Calculate Fibonacci sequence
        fib_sequence = fibonacci_sequence(n)

        # Display Fibonacci sequence
        st.subheader("Fibonacci Sequence:")
        st.write(fib_sequence)

        # Plot Fibonacci sequence dynamically
        fig = go.Figure()
        for i in range(1, n + 1):
            fig.add_trace(go.Scatter(x=list(range(i + 1)), y=fibonacci_sequence(i), mode="lines+markers", name=f"Fib({i})"))
        fig.update_layout(title="Fibonacci Sequence Visualization", xaxis_title="N", yaxis_title="Fib(N)")
        st.plotly_chart(fig)

    elif app_selection == "Longest Common Subsequence (LCS)":
        st.title("Longest Common Subsequence (LCS)")

        X = st.text_input("Enter sequence X:")
        Y = st.text_input("Enter sequence Y:")

        if st.button("Calculate LCS"):
            LCS_table = display_LCS_table(X, Y)
            LCS = get_LCS(X, Y, LCS_table)
            st.success(f"The Longest Common Subsequence is: {LCS}")

if __name__ == "__main__":
    main()
