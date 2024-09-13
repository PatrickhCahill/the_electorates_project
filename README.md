# The electorates project
This is the repository that will carry out the programming interface for my electorates project

## Overview
There are a few main purposes and therefore key functions associated with this codebase. The first is that there is no straightforward and easily accessible way of calculating the nominal voteshare of different divisions after redistributions.

In principle, this is a relatively straightforward thing to do. When a division changes shapes you subtract the votes from areas the are removed and add votes from areas that are added - this then allows you to determine the new nominal voteshare. 

In practice, this is a more complex question. The most naive way might be to simply compare boundaries and compute based on which polling places have been removed or added to the area. This works but is subject to error. **ENTER IN EXAMPLES HERE**

What we aim to do is to exptrapolate the estimated voteshare of each SA1 by using a weighted average of nearby polling places. This allows for a spatially continuous estimate of the voteshare.

Next, we approximate electoral divisions as a collections of SA1s. **Do we bother to spatially average or not?** We verify our approximations by using the previous election data and representation of the electorates. 

We are then able to take new electoral maps and compare how they have changed.

Finally, we implement algorithms associated with measuring the fairness of electoral boundaries. We develop helper functions that plot and measure the respective represenationa and proportionality of certain electoral maps.

## 1. Polling places to SA1s.
##### *Voting*
In Australia, federal elections are held up to three years apart. *Sort of...* The laws around the fluxation of a parliament are complicated, the rules around when a prime minister can call an election more so. But the general convention is that elections are held roughly three years apart. Voting is compulsory - if you are a registered voter, and nominally it is compulsory to be a registered voter. From here on out we will denote registered voters as *electors*.

When an election comes around *electors* must either vote or pay a fine. Turnout in Australia is high with most elections sitting around $90\%$. Work by Kos Samaras and others have looked at the effects of turnout on political parties. Most analyses tend to thank the stars that Australia has compulsory voting unlike most other countries and then move on.

Supposing that you do vote, you can vote in a number of different ways. You may cast one of the following:
- Ordinary vote
- Absent vote
- Provisional vote
- Declaration Pre-Poll vote
- Postal vote

**Ordinary vote**: By far the most common form of vote is the Ordinary vote. That is the vote where you go to your local school, church or public institution - what we call a *polling place* (PP) - in the division for which you enrolled,, nothing goes wrong with regards voter registration or the like, and cast a vote. Historically, this has been by the far the most common form of vote. 
> Suppose you are enrolled in the Division of Sydney. On election day you go to your local school or some other polling place in your division. You say your name and confirm your address. You cast vote. And at somepoint you buy a democracy sausage... the last part is optional.

It is also the vote that is counted on election night. Models like Antony Green's election night model for the ABC are based on extrapolating early swings from polling places to predict an overall picture of the night. This then allows the ABC to call the winner of elections in one division or another. However, these techniques have become more unreliable in recent years due to the rise in alternative vote methods.

**Pre-Poll Vote:** One distinction that is important from a media perspective but ignored from a data perspective is that there are two types of Ordinary votes. Election day Ordinary votes and Pre-Poll Ordinary votes. The difference is in the name. Pre-Poll Ordinary votes are cast before election day during a two-week long period where voting is optional for those who do not want to or cannot vote on election day. We call the polling places for Pre-Poll voting *Pre-Polling Voting Centres* (PPVC). Typically, the bulk of PPVC votes are counted late on election night, after the Election day Ordinary Votes are cast. Small differences in the behaviour of these different groups can be important for marginal seat contests.
> You live and are enrolled in the division of Menzies. You work Saturdays so the Monday before the election you go to your nearest Pre-Poll vote centre and cast your ballot.

**Postal Vote:** Postal Voting is similar to Pre-Poll voting in that votes are cast before election day. Individuals apply with the AEC to cast a Postal Vote who then return in the mail a ballot. The elector then writes their ballot and sends it in the mail to the AEC. These votes are less common than the Ordinary vote but grew in popularity during COVID. There is no polling place associated with them so it is difficult to determine wherefrom the ballots were cast. People who cast Postal votes tend to be older and historically have been more conservative. That said, the important thing is that again demographic differences between this vote type and the Ordinary Vote means that difference swings are possible. Postal votes can be received after election day with a certain timeframe. Therefore, they take longer to count. Many marginal seats may appear to be leaning one way on election night but swing the other way because of Postal Vote trends not accounted for.
> You are enrolled to vote in Bass. You are concerned for your health or some other reason which means you apply for a postal ballot. The AEC accepts your application and sends you a ballot. You cast your ballot and mail it to the AEC.


**Absent Votes:** Absent votes are votes cast by electors in divisions or locations outside of the division for which they are enrolled. 
> Suppose you live in the division of Adelaide, South Australia and are enrolled to vote there. You happen to be on holiday in Cairns, Queensland at the time of the election. If you go to a polling place in Cairns to vote, you would cast an absent vote. These are tied to polling places but the polling places do not generally give elections.


**Provision Vote:** Provisional votes are votes cast on election day where there is some dispute regarding the electoral roll. The votes are cast but kept separate from the Ordinary Votes so that they may be processed and checked before tallied.
> You are enrolled in the division of Cowper. Someone with a very similar name to you voted in the same polling place an hour ago. The AEC volunteer accidentally crossed your name off as having vote. You are willing to make a declaratation that you have not yet cast your ballot. You are given a provisional ballot instead of an ordinary ballot.

Situations such as describe in the sample above, or issues regarding the address of the elector may result in a declaration vote. They are both a safeguard to ensure the integrity of the vote count but also to preserve the democratic right of electors to cast their ballots.
**Declaration Pre-Poll:** Declaration Pre-Poll votes are much the same as above but are made during the Early Voting period prior to election day.
> You are enrolled in the division of Curtin. Its the Tuesday before the election. You've recently moved but still live in Curtin. You go to a polling place and give the new address when asked where you live. You must make a Declaration in order to vote so it is a Declaration Pre-Poll vote.

##### *Modelling*
We will restrict ourselves to considering a single state. Denote the list of $n$ different divisions in this state to be $E=
\{E_1, E_2, ..., E_n\}.$ Next denote the list of $m$ polling places to be $p=\{p_1,p_2,...,p_m\}.$ Further, let the list of $k$ SA1s be given by $S=\{s_1,s_2,...s_k\}$.

Each entity is to be considered a geographical subset of the space occupied by the single state. Hence, $s_2 \subset E_1$ implies that the SA1 $s_2$ is entirely contained within $E_1$. A polling place should be considered as a single point in the state.

Next, we have some simple facts. First, there is no overlap between any of the electorates, i.e $\forall i,j \le n, \; E_i \cap E_j = \empty.$ The equivalent statement is true for SA1s and naturally for polling places.

Second, for any electorate $E_i$ there exists a collection of SA1s such it is covered. Formerly, $\forall E_i\;\exists I $ such that $E_i \subseteq \cup_{\alpha \in I} s_\alpha,$ where $I$ is some indicator set. We denote the smallest such collection as $S_{E_i}.$

Third, 







1. Polling place to SA1s
2. Divisions to SA1s and back
3. Network Programming for Redistributions
