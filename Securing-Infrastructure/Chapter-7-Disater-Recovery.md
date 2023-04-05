# Chapter 7. Disaster Recovery


- *Business continuity planning (BCP)*: 
  - Pertains to the overall continuation of business via a number of contingencies and alternative plans
- *Disaster recovery (DR)*:
  - The set of processes and procedures that are used in order to reach the objectives of the Business Continuity Plan

## Setting Objectives

- Allow to 
  - Ensure that you are measurably meeting business
    requirements when creating a DR strategy
  - To more easily make decisions regarding balancing time and budget considerations against uptime and recovery times

- Recovery Point Objective: 
  - RPO is the point in time that you wish to recover to.

- Recovery Time Objective:
  - How long it takes to recover, taken irrespective of the RPO - After the disaster, how long until you have
  recovered to the point determined by the RPO.


## Recovery Strategies

- Depend on RTO (Recovery Time Objective), RPO ( Recovery Point Objective), cost.

- Backups:
  - The most obvious strategy for recovering from a disaster
  - Take backups of all systems and to restore those backups to new equipment
  - Have a longer RPO than other strategies
- Warm Standby:
  - A secondary infrastructure, keep in approximate synchronization with primary infrastructure
  - The RPO is fairly short, the RTO is however long the cut-over mechanism takes
- High Availability:
  - A model like a distributed cluster, 
- Alternate System
- System Function Reassignment

## Dependencies

- Understand the dependencies of all system is an important part of developing a strategy for DR and BCP.
  - By mapping out dependencies, it is much easier to identify unrealistic ROTs, or RTOs of other systems or services

# Scenarios

- Walk through a few high-level scenarios can help zp