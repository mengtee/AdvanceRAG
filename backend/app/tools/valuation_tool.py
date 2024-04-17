# define sample Tool
def calculate_intrinsic_value(fcf, growth_rate, discount_rate, terminal_rate, years, total_debt, shares_outstanding):
    """
    Calculate the intrinsic value of a company using the DCF method.
    
    :param fcf: Initial Free Cash Flow
    :param growth_rate: Growth rate of FCF for the forecast period
    :param discount_rate: Weighted Average Cost of Capital (WACC)
    :param terminal_rate: Growth rate into perpetuity after forecast period
    :param years: Number of years for the forecast period
    :param total_debt: Total debt of the company
    :param shares_outstanding: Number of shares outstanding
    :return: Intrinsic value per share
    """
    
    # Calculate the present value of forecasted FCFs
    present_value_fcf = sum(fcf * (1 + growth_rate)**i / (1 + discount_rate)**i for i in range(1, years + 1))
    
    # Calculate the terminal value
    final_year_fcf = fcf * (1 + growth_rate)**years
    terminal_value = final_year_fcf * (1 + terminal_rate) / (discount_rate - terminal_rate)
    
    # Discount the terminal value to present value
    present_value_terminal = terminal_value / (1 + discount_rate)**years
    
    # Calculate the total present value of all cash flows
    total_present_value = present_value_fcf + present_value_terminal
    
    # Adjust for debt and calculate value per share
    equity_value = total_present_value - total_debt
    intrinsic_value_per_share = equity_value / shares_outstanding
    
    return intrinsic_value_per_share
