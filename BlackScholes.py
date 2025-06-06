import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

class BlackScholes:
    def __init__(
        self, 
        vol: float, 
        underlyingPrice: float, 
        strikePrice: float, 
        timeToExp: int,
        riskFreeRate: float):

        self.volatility = vol
        self.underlying_Price = underlyingPrice
        self.strike_Price = strikePrice
        self.time_to_expiration = timeToExp
        self.risk_free_rate = riskFreeRate
    
    def calcPrice(self, option_type='call'):
        S, K, T, r, sigma = self.underlying_Price, self.strike_Price, self.time_to_expiration, self.risk_free_rate, self.volatility
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        if option_type == 'call':
            return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        else:
            return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    
    def monte_carlo_simulation(self, num_simulations=500):
        num_steps = 252
        dt = self.time_to_expiration / num_steps
        S = np.zeros((num_simulations, num_steps + 1))
        S[:, 0] = self.underlying_Price
        for t in range(1, num_steps + 1):
            Z = np.random.standard_normal(num_simulations)
            S[:, t] = S[:, t-1] * np.exp((self.risk_free_rate - 0.5 * self.volatility**2) * dt + self.volatility * np.sqrt(dt) * Z)
        
        # Calculate payoffs for both call and put options using the final stock prices
        final_stock_prices = S[:, -1]
        call_payoffs = np.maximum(final_stock_prices - self.strike_Price, 0)
        put_payoffs = np.maximum(self.strike_Price - final_stock_prices, 0)

        # Calculate discounted option prices
        call_option_price = np.exp(-self.risk_free_rate * self.time_to_expiration) * np.mean(call_payoffs)
        put_option_price = np.exp(-self.risk_free_rate * self.time_to_expiration) * np.mean(put_payoffs)

        return call_option_price, put_option_price, S

    def visualize(self, num_simulations=100):
        # Calculate theoretical price
        theoretical_price = self.calcPrice()
        
        # Run Monte Carlo simulation
        mc_price, _ = self.monte_carlo_simulation(num_simulations)
        
        # Create time points for x-axis
        time_points = np.linspace(0, self.time_to_expiration, paths.shape[1])
        
        # Plot the paths
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        for i in range(min(50, num_simulations)):  # Plot first 50 paths for clarity
            plt.plot(time_points, paths[i], alpha=0.2)
        plt.plot(time_points, np.mean(paths, axis=0), 'r-', linewidth=2, label='Average Path')
        plt.axhline(y=self.strike_Price, color='g', linestyle='--', label='Strike Price')
        plt.title('Monte Carlo Simulation Paths')
        plt.xlabel('Time')
        plt.ylabel('Stock Price')
        plt.legend()
        
        # Plot option price convergence
        plt.subplot(1, 2, 2)
        mc_prices = []
        for n in range(1, num_simulations + 1):
            mc_price, _ = self.monte_carlo_simulation(n)
            mc_prices.append(mc_price)
        
        plt.plot(range(1, num_simulations + 1), mc_prices, 'b-', label='Monte Carlo Price')
        plt.axhline(y=theoretical_price, color='r', linestyle='--', label='Theoretical Price')
        plt.title('Option Price Convergence')
        plt.xlabel('Number of Simulations')
        plt.ylabel('Option Price')
        plt.legend()
        
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    # Example usage
    bs = BlackScholes(
        vol=0.2,  # 20% volatility
        underlyingPrice=100,  # Current stock price
        strikePrice=100,  # Strike price
        timeToExp=1,  # 1 year to expiration
        riskFreeRate=0.05  # 5% risk-free rate
    )
    
    # Calculate theoretical price
    theoretical_price = bs.calcPrice()
    print(f"Theoretical Option Price: ${theoretical_price:.2f}")
    
    # Run Monte Carlo simulation
    mc_price, _ = bs.monte_carlo_simulation()
    print(f"Monte Carlo Option Price: ${mc_price:.2f}")
    
    # Visualize
    bs.visualize()
