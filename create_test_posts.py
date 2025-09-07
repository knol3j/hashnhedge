#!/usr/bin/env python3
"""
Create test posts with clean YAML to test infinite scroll
"""

import os
from datetime import datetime, timedelta

POSTS_DIR = "site/content/posts"

def create_test_posts():
    """Create 50 test posts for demonstration"""
    os.makedirs(POSTS_DIR, exist_ok=True)
    
    base_date = datetime(2025, 8, 23)
    
    posts = [
        ("bitcoin-price-analysis-august-2025", "Bitcoin Price Analysis: Market Trends in August 2025", "Crypto"),
        ("ethereum-2-staking-rewards-update", "Ethereum 2.0 Staking Rewards See Major Update", "Crypto"),
        ("defi-yield-farming-strategies", "Top DeFi Yield Farming Strategies for 2025", "DeFi"),
        ("nft-market-recovery-signals", "NFT Market Shows Strong Recovery Signals", "Markets"),
        ("solana-ecosystem-growth", "Solana Ecosystem Experiences Unprecedented Growth", "Crypto"),
        ("cardano-smart-contracts-upgrade", "Cardano Smart Contracts Get Major Upgrade", "Crypto"),
        ("polygon-scaling-solutions", "Polygon Introduces New Scaling Solutions", "Technology"),
        ("chainlink-oracle-expansion", "Chainlink Expands Oracle Network Globally", "Technology"),
        ("uniswap-governance-proposal", "Uniswap Governance Passes Important Proposal", "DeFi"),
        ("compound-lending-rates", "Compound Lending Rates Hit New Highs", "DeFi"),
        ("aave-flash-loans-record", "AAVE Flash Loans Reach Record Volume", "DeFi"),
        ("binance-regulatory-compliance", "Binance Enhances Regulatory Compliance Framework", "Markets"),
        ("coinbase-institutional-services", "Coinbase Launches New Institutional Services", "Markets"),
        ("metamask-mobile-update", "MetaMask Mobile Gets Security Enhancement", "Technology"),
        ("ledger-hardware-wallet", "Ledger Releases Next-Gen Hardware Wallet", "Security"),
        ("crypto-tax-regulations", "New Crypto Tax Regulations Take Effect", "Regulation"),
        ("central-bank-digital-currency", "Central Bank Digital Currency Pilots Expand", "Regulation"),
        ("stablecoin-market-analysis", "Stablecoin Market Reaches $150 Billion", "Markets"),
        ("layer-2-adoption-growth", "Layer 2 Solutions See Massive Adoption Growth", "Technology"),
        ("web3-social-media-rise", "Web3 Social Media Platforms Gain Traction", "Social"),
        ("dao-governance-trends", "DAO Governance Models Evolution in 2025", "Governance"),
        ("crypto-gaming-boom", "Crypto Gaming Industry Experiences Boom", "Gaming"),
        ("institutional-bitcoin-buying", "Institutional Bitcoin Buying Reaches ATH", "Markets"),
        ("energy-efficient-mining", "Energy-Efficient Mining Technologies Emerge", "Mining"),
        ("cross-chain-interoperability", "Cross-Chain Interoperability Solutions Launch", "Technology"),
        ("quantum-resistance-crypto", "Quantum-Resistant Cryptography Development", "Security"),
        ("tokenomics-design-trends", "Tokenomics Design Trends for 2025", "Economics"),
        ("yield-optimization-protocols", "New Yield Optimization Protocols Launch", "DeFi"),
        ("insurance-protocols-growth", "Crypto Insurance Protocols See Growth", "Insurance"),
        ("prediction-markets-evolution", "Prediction Markets Evolution and Trends", "Markets"),
        ("synthetic-assets-platform", "Synthetic Assets Platform Launches", "DeFi"),
        ("liquidity-mining-rewards", "Liquidity Mining Rewards Optimization", "DeFi"),
        ("governance-token-analysis", "Governance Token Analysis and Trends", "Governance"),
        ("automated-market-makers", "Automated Market Makers Innovation", "Technology"),
        ("flash-loan-arbitrage", "Flash Loan Arbitrage Opportunities", "Trading"),
        ("impermanent-loss-solutions", "Solutions for Impermanent Loss", "DeFi"),
        ("crypto-derivatives-market", "Crypto Derivatives Market Expansion", "Trading"),
        ("options-trading-platforms", "Options Trading Platforms Launch", "Trading"),
        ("perpetual-swaps-innovation", "Perpetual Swaps See Innovation", "Trading"),
        ("margin-trading-safety", "Margin Trading Safety Improvements", "Trading"),
        ("algorithmic-trading-bots", "Algorithmic Trading Bots Evolution", "Technology"),
        ("market-making-strategies", "Market Making Strategies for 2025", "Trading"),
        ("portfolio-management-tools", "Portfolio Management Tools Update", "Tools"),
        ("risk-management-protocols", "Risk Management Protocols Launch", "Security"),
        ("compliance-automation-tools", "Compliance Automation Tools", "Regulation"),
        ("kyc-aml-solutions", "KYC/AML Solutions for DeFi", "Compliance"),
        ("audit-security-standards", "Audit and Security Standards Update", "Security"),
        ("bug-bounty-programs", "Bug Bounty Programs Expansion", "Security"),
        ("smart-contract-verification", "Smart Contract Verification Tools", "Security"),
        ("blockchain-analytics-tools", "Blockchain Analytics Tools Launch", "Analytics")
    ]
    
    for i, (slug, title, category) in enumerate(posts):
        post_date = base_date - timedelta(days=i)
        
        content = f'''---
title: "{title}"
date: "{post_date.strftime('%Y-%m-%dT%H:%M:%S')}"
category: "{category}"
summary: "Latest developments and analysis in the {category.lower()} space with expert insights and market trends."
image: "/images/posts/{slug}.svg"
seo:
  title: "{title} | Hash & Hedge"
  description: "Expert analysis on {title.lower()} with market insights and trends"
  keywords: ["{category.lower()}", "cryptocurrency", "blockchain", "analysis"]
---

# {title}

This is a comprehensive analysis of recent developments in the {category.lower()} sector. Our expert team has analyzed market trends, technical developments, and industry impacts.

## Key Highlights

- Market analysis shows significant trends in {category.lower()}
- Technical developments are shaping the future landscape  
- Industry adoption continues to accelerate
- Regulatory clarity is improving market confidence

## Market Impact

The {category.lower()} sector has shown remarkable resilience and growth potential. Key metrics indicate:

* Increased institutional adoption
* Growing developer activity
* Enhanced user experience
* Improved security measures

## Expert Analysis

Our research team believes this development represents a significant milestone for the {category.lower()} industry. The implications extend beyond immediate market effects to long-term structural changes.

## Looking Forward

As we monitor these developments, several factors will be crucial:

1. **Regulatory Environment**: Continued clarity from regulators
2. **Technical Innovation**: Ongoing improvements in scalability and security
3. **Market Adoption**: Broader acceptance by traditional institutions
4. **User Experience**: Enhanced accessibility for mainstream users

## Conclusion

This analysis highlights the dynamic nature of the {category.lower()} space and the importance of staying informed about rapid developments in this evolving sector.

*This analysis is for informational purposes only and does not constitute financial advice.*
'''
        
        filename = f"{slug}.md"
        filepath = os.path.join(POSTS_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"Created {len(posts)} test posts")

if __name__ == "__main__":
    create_test_posts()