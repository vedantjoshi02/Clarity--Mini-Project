const assert=require('node:assert/strict'),M=require('../dist/math.js');
const near=(a,b)=>assert.ok(Math.abs(a-b)<Math.max(1e-6,Math.abs(b)*1e-10),`${a} ≠ ${b}`);
near(M.value(100000,10,3,'compound',1),133100);
near(M.value(100000,10,3,'simple',1),130000);
near(M.value(100000,12,1,'compound',12),112682.50301319698);
near(M.value(100000,8,2,'compound',4),117165.93810022656);
near(M.value(100000,0,30,'compound',12),100000);
near(M.requiredRate(100000,30000,3,'simple'),10);
near(M.requiredRate(100000,33100,3,'compound'),10);
near(M.requiredRate(100000,0,3,'compound'),0);
for(const type of ['simple','compound'])for(const frequency of [1,4,12]){const rate=M.requiredRate(250000,75000,5,type,frequency);near(M.value(250000,rate,5,type,frequency),325000)}
let result=M.schedule({principal:100000,rate:10,profit:30000,years:3,type:'compound',frequency:1,solve:'profit'});assert.equal(result.rows.length,4);near(result.rows[0].balance,100000);near(result.rows[3].profit,33100);
result=M.schedule({principal:100000,rate:0,profit:30000,years:3,type:'compound',frequency:12,solve:'rate'});near(result.rows[3].balance,130000);assert.ok(result.rows.every((r,i,a)=>!i||r.balance>=a[i-1].balance));
assert.throws(()=>M.requiredRate(0,30000,3));assert.throws(()=>M.requiredRate(100000,30000,0));assert.throws(()=>M.value(100000,NaN,3));
console.log('22 mathematical checks passed');
