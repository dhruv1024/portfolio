Based on following parameters, create a formula to calculate the probability of any on man getting married based on age range and the same for women?

Assumming that male and female ratio is 50-50
A person has to get married between 20 and 50 years of age, becoming eligible at 20 and stopping trying to find a spouse at 50 due to old age
A person is more attractive if young and rich for men and beautiful for women

Guys almost always marry down
Both genders want top 1% of attractiveness(calculated as mentioned above)
People marry within 5 year range of themsleves, thus limiting their options unless they are in extremes of the attractiness spectrum.

Assumming that 50% of marriages end in divorce, similarly 50% of second marriages end in divorce and so on
Men lose 50% of their savings in divorce and thus take a big hit in attractiveness
Women unless they have a child, gain attractiveness due to wealth, otherwise gain 5 years in age due to the child - ultimately losing attractiveness

Porn is causing promiscuous women to be richer, which generally makes them unattractive. This option is usually chosen by women who aren't rich but young.

The weightage becomes expoential at extremes of a factor i.e. everyone wants to marry someone with 0.99 attractiveness or beauty or wealth whereas no one wants to marry someone with 0.01 attractiveness or beauty or wealth, its not linear or a matter of probability.

2. Also, change in probability with changing any factor is very less, can you improve the code accordingly?
3. Lastly, the probability is still maxed at age 35 due to the setup. I expect the age to vary based on the given factors like attractiveness, age(given attractiveness decreases with age and there are less women too marry)

Also, add a tenet that unless the person is in extremes of the attractiness spectrum they marry within 5 year range of themsleves, thus limiting their options.

Creating precise weights without accurate data is challenging, and any estimates provided would be highly speculative. However, I can offer a simplified, conceptual representation based on common societal trends. Keep in mind that these are broad generalizations and may not accurately reflect individual experiences or cultural variations.

Let's assign arbitrary weights to the factors mentioned earlier and provide a conceptual overview of how probabilities might vary across age groups:

1. **Base Attractiveness:**
   - Younger age (20-30): Weight = 0.4
   - Middle age (30-40): Weight = 0.3
   - Older age (40-50): Weight = 0.2

2. **Wealth Factor:**
   - Younger age (20-30): Weight = 0.2
   - Middle age (30-40): Weight = 0.3
   - Older age (40-50): Weight = 0.4

3. **Beauty Factor:**
   - Younger age (20-30): Weight = 0.3
   - Middle age (30-40): Weight = 0.2
   - Older age (40-50): Weight = 0.1

4. **Divorce Factor:**
   - Younger age (20-30): Weight = 0.1
   - Middle age (30-40): Weight = 0.3
   - Older age (40-50): Weight = 0.5

5. **Child Factor:**
   - Younger age (20-30): Weight = 0.3
   - Middle age (30-40): Weight = 0.4
   - Older age (40-50): Weight = 0.2

6. **Porn Factor:**
   - Younger age (20-30): Weight = 0.2
   - Middle age (30-40): Weight = 0.3
   - Older age (40-50): Weight = 0.4

Now, let's construct the probability formula for men:

\[ P_{\text{man}} = \frac{{0.4 \cdot \text{Base Attractiveness}_{\text{man}} + 0.2 \cdot \text{Wealth Factor}_{\text{man}} + 0.3 \cdot \text{Beauty Factor}_{\text{man}} - 0.1 \cdot \text{Divorce Factor}_{\text{man}} - 0.2 \cdot \text{Porn Factor}_{\text{man}}}}{{\text{Normalization Factor}_{\text{man}}}} \]

And similarly for women:

\[ P_{\text{woman}} = \frac{{0.3 \cdot \text{Base Attractiveness}_{\text{woman}} + 0.4 \cdot \text{Wealth Factor}_{\text{woman}} + 0.2 \cdot \text{Beauty Factor}_{\text{woman}} + 0.2 \cdot \text{Child Factor}_{\text{woman}} - 0.5 \cdot \text{Divorce Factor}_{\text{woman}} - 0.3 \cdot \text{Porn Factor}_{\text{woman}}}}{{\text{Normalization Factor}_{\text{woman}}}} \]

Without specific data and a more detailed analysis, it's challenging to provide an accurate percentage for the probability of marriage for a person with the given characteristics. However, I can provide a simplified example of how you might approach this using the conceptual formula we discussed earlier.

Let's assume the following subjective ratings for the individual:

- Base Attractiveness: 0.7 (above average height and looks)
- Wealth Factor: 0.3 (lower middle-class income)
- Beauty Factor: 0.6 (subjective rating)
- Divorce Factor: 0.1 (never married)
- Child Factor: 0 (no children)
- Porn Factor: 0 (not involved in the porn industry)

Now, let's plug these values into the formula for men:

\[ P_{\text{man}} = \frac{{0.4 \cdot 0.7 + 0.2 \cdot 0.3 + 0.3 \cdot 0.6 - 0.1 \cdot 0 - 0.2 \cdot 0}}{{\text{Normalization Factor}_{\text{man}}}} \]

For simplicity, let's assume \(\text{Normalization Factor}_{\text{man}}\) is 1.

\[ P_{\text{man}} = \frac{{0.28 + 0.06 + 0.18}}{{1}} \]

\[ P_{\text{man}} = 0.52 \]

So, in this simplified example, the estimated probability for this 26-year-old man to get married might be 52%. Keep in mind that these weights and factors are arbitrary and would need adjustment based on real data and a more sophisticated analysis. Additionally, individual preferences and circumstances can vary widely, making it challenging to accurately predict such outcomes.
