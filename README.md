# Why this soultion for Timer smart contract is the best?
**It is the cheapest solution (of those not based on tick-tock mechanism).**

We spend a huge efforts to optimize computations (that is why contract is written in close to assembler low-level language) and to research possible options to make contract cheaper (see below). With cost <= 50 Gram/day we dare to say that it is the cheapest solution in the wild.

**It is most general**

It works with TON primitives: messages and cells; thus is compatible with all languages and frameworks.

**Unlimited application and correct economical model**

Since this contract may schedule arbitrary message to send at desired time, it can be used not only to notify contract about the time, but without changing can be used for any high-level scenarios. For instance send message to yourself, to call any desired method of the contract in the future, to deploy contract in the future etc. Special attention is paid to economical model. That way contract correcly charge for storage and also check outgoing message for correct amounts. Thus, it is already suitable for work not only with grams, but also with native tokens.

==========================================
# Problem
In general, there are no schedulers in TON; one cannot ask a contract to execute some code in a year or 5 blocks later, etc. 
It is possible to make a third-party service off-chain that will pull specified contract on schedule, but reliability is always in question.
In Ethereum, this problem is unsolvable onchain, but TON is different. 

# Solution: general scheduler
Calls between contracts are not synchronous; if contract A sends a message to contract B, the second one will not receive it immediately. Thus, by building a looped chain of such messages, we can make the contract to wake up regularly and do something: for instance check whether it is a time to send scheduled message.

### General vs special scheduler
General scheduler which spends gas for work may be quite expensive. However anybody can deploy one without cooperation with anybody else. Alternative solution which based on tick-tock special contracts is available in the other repository. While special contract soultion doesn't require gas for work, it however requires cooperation of validators to instantiate such contract. Thus while both solutions have pros and cons they are not mutually exclusive: both are suitable for their niches.

# Detailed scheme
1. Smart contract sends message to address which will bounce it back. 
2. On each bounce from step 1, scheduler check it's table of scheduled messages. 
3. If there are messages which are ready to be send, scheduler sends them.
4. If there are scheduled message in table scheduler sends new message to be bounced (thus starting new iteration).
5. If scheduler recieve message from the other contract it treats that message as request for scheduling. It reads time for scheduling and message to be sent. Then it rewrites message to be sent and sets correct gram and native token amounts and store in the table.

### Bounce scheme
Upon developing we came to three possible solutions for bouncing.
1. Use general contract at the bouncing side
2. Use special contract at the bouncing side
3. Use uninit contract at the bouncing side
In first option one contract receive message and manually sends it back. However it is allways more expensive than sending to uninit contract (third option) since it requires at least some computations. Second one is idea to exploit one of the special contract to save some gas (since special contracts does not require gas for computations. In particular, it is possible to use "unknown query" https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/elector-code.fc#L668 response in elector contract. Indeed, this bounce does not require gas for computations and even save 0.01 gram for bounce. However costs of sending message to masterchain outweight advantages of this approach. That way autobounce from uninit account in basechain is a cheapest option.
#### Exact account address for bounce
We studied delays of sending messages from/to different shards. Generally there should be difference due to `next-hop` scheme of hypercube routing. Thus it principle it would possible to shorten/extend loop iteration duration by appropriate choice of destination shard. For instance if we know that next call is scheduled soon we will choose short iteration duration, otherwise we will choose longest duration by sending to most distant shard. Unfortunately, our study has shown, that for 16 shards (current number of shards in basechain) difference is negligible. So we didn't include code for iteration duration control into solution yet.

# Why FunC?
There are bunch of languages and compillators supported by TON Labs which are more cosy and pleasant for developing complex smartcontracts. Why develop this contract in FunC? The pleasure of working with high-level languages comes at a price:

1. Direct gas price: FunC are close to bare metal and thus allows unimaginable for other languages optimizations. Since scheduler constantly comsume gas - it is very important.
2. Generality. This solution works with native TON primitives such as messages and cells. It doesn't depends on Solc ABI etc. It means that proposed solution will work both with C, Solc and other codebases. And even will work with languages which are not yet developed. It is quite hard to achieve the same level of generality using high-level languages.



