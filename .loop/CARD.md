# Card #15: [Card] ignition-probe-1

**ID:** ignition-probe-1
**Tier:** trivial
**Role:** impl
**Paths:** ignition/impl-1/**
**Forbidden:** .github/**, **/*.lock, settings/**

## Acceptance Criteria
1. ignition/impl-1/probe.txt 存在且内容为 ignition ok
2. ignition/impl-1/status.txt 含 === loopd status === 行
3. ignition/impl-1/tail.txt 不含 UNKNOWN_INTENT

## Body

