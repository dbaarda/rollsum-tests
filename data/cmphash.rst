=== ==== ======= ==================================================== =========================       =========================      
dat   bs   count rollsum                                              hash min/max/col/perf           cluster min/max/col/perf       
=== ==== ======= ==================================================== =========================       =========================      
csv   32  867187 CyclicPoly(seed=0, offs=0, map=mix)                  0/2/0.000100/1.000001           2/30/0.924427/1.002632         
csv   32  867187 RabinKarp(seed=0, offs=0, map=pow, mult=0x8104225)   0/2/0.000105/0.999992           1/30/0.924427/1.005921         
csv   32  867187 RabinKarp(seed=0, offs=0, map=pow, mult=0x41c64e6d)  0/2/0.000106/0.999990           1/31/0.924427/0.997412         
csv   32  867187 RabinKarp(seed=0, offs=0, map=mul, mult=0x41c64e6d)  0/2/0.000112/0.999978           1/30/0.924427/1.000420         
csv   32  867187 RabinKarp(seed=0, offs=0, map=ord, mult=0x41c64e6d)  0/2/0.000112/0.999978           2/33/0.924427/0.973518         
csv   32  867187 RabinKarp(seed=0, offs=0, map=mul, mult=0x8104225)   0/2/0.000114/0.999974           2/32/0.924427/0.995039         
csv   32  867187 RabinKarp(seed=0, offs=1, map=ord, mult=0x8104225)   0/2/0.000114/0.999974           0/35/0.924428/0.963930         
csv   32  867187 RabinKarp(seed=0, offs=0, map=ord, mult=0x8104225)   0/2/0.000114/0.999974           0/35/0.924428/0.963930         
csv   32  867187 RabinKarp(seed=1, offs=0, map=ord, mult=0x8104225)   0/2/0.000114/0.999974           1/33/0.924427/0.962215         
csv   32  867187 CyclicPoly(seed=0, offs=0, map=ipfs)                 0/2/0.000122/0.999957           1/33/0.924427/1.012661         
csv   32  867187 CyclicPoly(seed=0, offs=0, map=mul)                  0/3/0.000710/0.998755           1/39/0.924427/0.948402         
csv   32  867187 RollSum(seed=1, offs=0, map=pow, base=0x10000)       0/3/0.002139/0.995865           0/188/0.980210/0.012369        
csv   32  867187 RabinKarp(seed=0, offs=0, map=pow, mult=0x55555555)  0/5/0.008495/0.981261           1/31/0.924427/0.944960         
csv   32  867187 CyclicPoly(seed=0, offs=0, map=pow)                  0/6/0.010079/0.978636           0/2427/0.924430/0.018436       
csv   32  867187 RabinKarp(seed=0, offs=0, map=pow, mult=0xfffffffd)  0/7/0.010481/0.975848           1/33/0.924427/0.961240         
csv   32  867187 RabinKarp(seed=0, offs=0, map=mul, mult=0x55555555)  0/167/0.077168/0.617611         1/177/0.924427/0.609078        
csv   32  867187 RabinKarp(seed=0, offs=0, map=ord, mult=0x55555555)  0/167/0.077168/0.617611         1/396/0.924427/0.294158        
csv   32  867187 RabinKarp(seed=0, offs=0, map=mul, mult=0xfffffffd)  0/209/0.086626/0.526591         0/223/0.924430/0.499917        
csv   32  867187 RabinKarp(seed=0, offs=0, map=ord, mult=0xfffffffd)  0/209/0.086626/0.526591         1/694/0.924427/0.145060        
csv   32  867187 CyclicPoly(seed=0, offs=0, map=ord)                  0/80/0.139324/0.288086          0/35347/0.924700/0.000355      
csv   32  867187 Gear(offs=0, map=mix)                                0/410/0.082851/0.134621         0/33362/0.924444/0.000386      
csv   32  867187 RollSum(seed=1, offs=0, map=mul, base=0x10000)       0/36/0.770457/0.124251          0/833/0.994813/0.001882        
csv   32  867187 RollSum(seed=1, offs=0, map=ord, base=0x10000)       0/36/0.770457/0.124251          0/11527/0.999171/0.000117      
csv   32  867187 RollSum(seed=0, offs=31, map=ord, base=0x10000)      0/36/0.770457/0.124251          0/11636/0.999169/0.000117      
csv   32  867187 Gear(offs=0, map=mul)                                0/368/0.169487/0.113071         0/33180/0.924569/0.000381      
csv   32  867187 Gear(offs=0, map=ord)                                0/368/0.169487/0.113071         0/36285/0.924901/0.000339      
csv   32  867187 Gear(offs=0, map=ipfs)                               0/643/0.089414/0.096232         0/35838/0.924444/0.000328      
csv   1K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0x41c64e6d)  0/2/0.000097/1.000039           2/34/0.934464/1.000183         
csv   1K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0x8104225)   0/2/0.000103/1.000027           2/33/0.934464/1.009847         
csv   1K 1000000 RabinKarp(seed=1, offs=0, map=ord, mult=0x8104225)   0/2/0.000108/1.000017           2/32/0.934464/0.999539         
csv   1K 1000000 RabinKarp(seed=0, offs=1, map=ord, mult=0x8104225)   0/2/0.000108/1.000017           2/33/0.934464/0.998063         
csv   1K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0x8104225)   0/2/0.000108/1.000017           2/33/0.934464/0.998063         
csv   1K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0xfffffffd)  0/2/0.000108/1.000017           1/36/0.934464/0.994919         
csv   1K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0x8104225)   0/2/0.000108/1.000017           1/34/0.934464/0.987189         
csv   1K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0x55555555)  0/2/0.000114/1.000005           2/32/0.934464/1.003159         
csv   1K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0x55555555)  0/2/0.000126/0.999981           1/37/0.934464/1.008411         
csv   1K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0x55555555)  0/2/0.000126/0.999981           2/36/0.934464/0.999146         
csv   1K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0x41c64e6d)  0/2/0.000129/0.999975           2/34/0.934464/1.002067         
csv   1K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0x41c64e6d)  0/2/0.000129/0.999975           2/33/0.934464/0.999206         
csv   1K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0xfffffffd)  0/2/0.000139/0.999955           2/35/0.934464/1.002529         
csv   1K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0xfffffffd)  0/2/0.000139/0.999955           2/36/0.934464/1.001989         
csv   1K 1000000 RollSum(seed=1, offs=0, map=pow, base=0x10000)       0/3/0.000170/0.999875           0/73/0.934475/0.300622         
csv   1K 1000000 CyclicPoly(seed=0, offs=0, map=ipfs)                 0/2/0.003791/0.992704           2/33/0.934464/0.992776         
csv   1K 1000000 CyclicPoly(seed=0, offs=0, map=pow)                  0/3/0.003792/0.992701           2/36/0.934464/0.989177         
csv   1K 1000000 CyclicPoly(seed=0, offs=0, map=ord)                  0/2/0.003798/0.992691           1/36/0.934464/0.943160         
csv   1K 1000000 CyclicPoly(seed=0, offs=0, map=mix)                  0/3/0.003799/0.992687           2/36/0.934464/0.995319         
csv   1K 1000000 CyclicPoly(seed=0, offs=0, map=mul)                  0/3/0.007376/0.985681           2/36/0.934464/0.986126         
csv   1K 1000000 RollSum(seed=1, offs=0, map=mul, base=0x10000)       0/3/0.011695/0.977157           0/220/0.979943/0.012106        
csv   1K 1000000 RollSum(seed=1, offs=0, map=ord, base=0x10000)       0/3/0.011695/0.977157           0/2347/0.997533/0.000656       
csv   1K 1000000 RollSum(seed=0, offs=31, map=ord, base=0x10000)      0/3/0.011695/0.977157           0/2335/0.997530/0.000656       
csv   4K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0x55555555)  0/2/0.000114/1.000005           1/35/0.934464/1.002785         
csv   4K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0xfffffffd)  0/2/0.000120/0.999993           2/34/0.934464/0.999527         
csv   4K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0x8104225)   0/2/0.000121/0.999991           2/36/0.934464/1.000790         
csv   4K 1000000 RabinKarp(seed=0, offs=1, map=ord, mult=0x8104225)   0/2/0.000121/0.999991           2/35/0.934464/0.987833         
csv   4K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0x8104225)   0/2/0.000121/0.999991           2/35/0.934464/0.987833         
csv   4K 1000000 RabinKarp(seed=1, offs=0, map=ord, mult=0x8104225)   0/2/0.000121/0.999991           2/34/0.934464/0.985514         
csv   4K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0x55555555)  0/2/0.000123/0.999987           2/36/0.934464/1.008362         
csv   4K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0x41c64e6d)  0/2/0.000123/0.999987           1/34/0.934464/1.005443         
csv   4K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0x55555555)  0/2/0.000123/0.999987           2/35/0.934464/1.001746         
csv   4K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0x41c64e6d)  0/2/0.000124/0.999985           3/38/0.934464/1.004687         
csv   4K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0xfffffffd)  0/2/0.000124/0.999985           2/32/0.934464/1.002154         
csv   4K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0x41c64e6d)  0/2/0.000124/0.999985           2/35/0.934464/1.001415         
csv   4K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0xfffffffd)  0/2/0.000124/0.999985           1/35/0.934464/0.993438         
csv   4K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0x8104225)   0/2/0.000127/0.999979           2/33/0.934464/0.997286         
csv   4K 1000000 RollSum(seed=1, offs=0, map=pow, base=0x10000)       0/21/0.000150/0.999553          2/71/0.934464/0.599289         
csv   4K 1000000 CyclicPoly(seed=0, offs=0, map=ipfs)                 0/3/0.003864/0.992559           2/32/0.934464/0.996791         
csv   4K 1000000 CyclicPoly(seed=0, offs=0, map=pow)                  0/3/0.003892/0.992501           2/35/0.934464/0.983678         
csv   4K 1000000 CyclicPoly(seed=0, offs=0, map=mix)                  0/3/0.003906/0.992474           2/36/0.934464/0.996190         
csv   4K 1000000 CyclicPoly(seed=0, offs=0, map=ord)                  0/3/0.003918/0.992450           2/36/0.934464/0.960520         
csv   4K 1000000 RollSum(seed=1, offs=0, map=mul, base=0x10000)       0/3/0.006288/0.987739           0/141/0.964088/0.026768        
csv   4K 1000000 RollSum(seed=0, offs=31, map=ord, base=0x10000)      0/3/0.006288/0.987739           0/1304/0.996393/0.001248       
csv   4K 1000000 RollSum(seed=1, offs=0, map=ord, base=0x10000)       0/3/0.006288/0.987739           0/1286/0.996392/0.001248       
csv   4K 1000000 CyclicPoly(seed=0, offs=0, map=mul)                  0/3/0.007878/0.984708           3/35/0.934464/0.986920         
csv  16K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0x41c64e6d)  0/2/0.000107/1.000019           3/34/0.934464/1.004873         
csv  16K 1000000 RabinKarp(seed=1, offs=0, map=ord, mult=0x8104225)   0/2/0.000114/1.000005           2/34/0.934464/1.006556         
csv  16K 1000000 RabinKarp(seed=0, offs=1, map=ord, mult=0x8104225)   0/2/0.000114/1.000005           3/34/0.934464/1.002101         
csv  16K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0x8104225)   0/2/0.000114/1.000005           3/34/0.934464/1.002101         
csv  16K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0x8104225)   0/2/0.000114/1.000005           2/35/0.934464/0.999208         
csv  16K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0xfffffffd)  0/2/0.000115/1.000003           2/34/0.934464/0.985027         
csv  16K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0x41c64e6d)  0/2/0.000118/0.999997           2/35/0.934464/1.007661         
csv  16K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0x41c64e6d)  0/2/0.000118/0.999997           2/33/0.934464/0.998932         
csv  16K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0x55555555)  0/2/0.000119/0.999995           1/35/0.934464/1.005382         
csv  16K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0x55555555)  0/2/0.000119/0.999995           2/33/0.934464/0.996184         
csv  16K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0x8104225)   0/2/0.000121/0.999991           2/33/0.934464/1.008735         
csv  16K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0xfffffffd)  0/2/0.000123/0.999987           2/33/0.934464/1.007885         
csv  16K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0xfffffffd)  0/2/0.000123/0.999987           2/33/0.934464/0.996418         
csv  16K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0x55555555)  0/2/0.000125/0.999983           2/34/0.934464/1.004384         
csv  16K 1000000 RollSum(seed=1, offs=0, map=pow, base=0x10000)       0/3/0.000126/0.999977           1/71/0.934464/0.596304         
csv  16K 1000000 RollSum(seed=1, offs=0, map=mul, base=0x10000)       0/6/0.003141/0.993851           0/96/0.958488/0.072398         
csv  16K 1000000 RollSum(seed=0, offs=31, map=ord, base=0x10000)      0/6/0.003141/0.993851           0/677/0.994480/0.002572        
csv  16K 1000000 RollSum(seed=1, offs=0, map=ord, base=0x10000)       0/6/0.003141/0.993851           0/668/0.994481/0.002571        
csv  16K 1000000 CyclicPoly(seed=0, offs=0, map=ipfs)                 0/2/0.003585/0.993111           2/34/0.934464/0.985386         
csv  16K 1000000 CyclicPoly(seed=0, offs=0, map=ord)                  0/2/0.003593/0.993095           2/36/0.934464/0.947026         
csv  16K 1000000 CyclicPoly(seed=0, offs=0, map=pow)                  0/3/0.003593/0.993093           2/35/0.934464/0.996722         
csv  16K 1000000 CyclicPoly(seed=0, offs=0, map=mix)                  0/3/0.003608/0.993059           3/33/0.934464/0.989277         
csv  16K 1000000 CyclicPoly(seed=0, offs=0, map=mul)                  0/2/0.006830/0.986751           1/38/0.934464/0.993119         
csv  64K 1000000 RabinKarp(seed=0, offs=1, map=ord, mult=0x8104225)   0/2/0.000106/1.000021           2/34/0.934464/1.008171         
csv  64K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0x8104225)   0/2/0.000106/1.000021           2/34/0.934464/1.008171         
csv  64K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0x8104225)   0/2/0.000106/1.000021           2/35/0.934464/1.006335         
csv  64K 1000000 RabinKarp(seed=1, offs=0, map=ord, mult=0x8104225)   0/2/0.000106/1.000021           3/35/0.934464/1.005016         
csv  64K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0x8104225)   0/2/0.000108/1.000017           2/36/0.934464/0.999082         
csv  64K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0x41c64e6d)  0/2/0.000113/1.000007           1/33/0.934464/0.997762         
csv  64K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0x41c64e6d)  0/2/0.000113/1.000007           2/36/0.934464/0.997326         
csv  64K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0x41c64e6d)  0/2/0.000119/0.999995           2/33/0.934464/0.997302         
csv  64K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0xfffffffd)  0/2/0.000121/0.999991           3/36/0.934464/0.999531         
csv  64K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0x55555555)  0/2/0.000122/0.999989           2/33/0.934464/1.007460         
csv  64K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0x55555555)  0/2/0.000122/0.999989           2/35/0.934464/1.004328         
csv  64K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0xfffffffd)  0/2/0.000122/0.999989           2/35/0.934464/0.999210         
csv  64K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0xfffffffd)  0/2/0.000122/0.999989           2/32/0.934464/0.998826         
csv  64K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0x55555555)  0/2/0.000128/0.999977           1/32/0.934464/1.004739         
csv  64K 1000000 RollSum(seed=1, offs=0, map=pow, base=0x10000)       0/9/0.000129/0.999815           2/66/0.934464/0.604432         
csv  64K 1000000 RollSum(seed=1, offs=0, map=mul, base=0x10000)       0/3/0.001527/0.997183           0/92/0.956036/0.088536         
csv  64K 1000000 RollSum(seed=1, offs=0, map=ord, base=0x10000)       0/3/0.001527/0.997183           0/362/0.992228/0.005551        
csv  64K 1000000 RollSum(seed=0, offs=31, map=ord, base=0x10000)      0/3/0.001527/0.997183           0/368/0.992231/0.005551        
csv  64K 1000000 CyclicPoly(seed=0, offs=0, map=mix)                  0/2/0.003702/0.992880           2/34/0.934464/0.983187         
csv  64K 1000000 CyclicPoly(seed=0, offs=0, map=pow)                  0/2/0.003715/0.992854           2/35/0.934464/0.993269         
csv  64K 1000000 CyclicPoly(seed=0, offs=0, map=ipfs)                 0/2/0.003728/0.992829           2/35/0.934464/0.994994         
csv  64K 1000000 CyclicPoly(seed=0, offs=0, map=ord)                  0/3/0.003741/0.992801           2/37/0.934464/0.959729         
csv  64K 1000000 CyclicPoly(seed=0, offs=0, map=mul)                  0/2/0.007298/0.985840           2/36/0.934464/0.978875         
zip   32  999977 RabinKarp(seed=0, offs=0, map=mul, mult=0x55555555)  0/2/0.000111/1.000011           2/33/0.934462/1.001297         
zip   32  999977 RabinKarp(seed=0, offs=0, map=ord, mult=0x55555555)  0/2/0.000111/1.000011           2/33/0.934462/0.993217         
zip   32  999977 RabinKarp(seed=0, offs=0, map=pow, mult=0x55555555)  0/2/0.000113/1.000007           1/33/0.934462/0.989824         
zip   32  999977 Gear(offs=0, map=mix)                                0/2/0.000114/1.000005           2/35/0.934462/0.998037         
zip   32  999977 RabinKarp(seed=0, offs=0, map=mul, mult=0x8104225)   0/2/0.000116/1.000001           2/37/0.934462/1.001503         
zip   32  999977 RabinKarp(seed=0, offs=1, map=ord, mult=0x8104225)   0/2/0.000116/1.000001           2/34/0.934462/1.000772         
zip   32  999977 RabinKarp(seed=0, offs=0, map=ord, mult=0x8104225)   0/2/0.000116/1.000001           2/34/0.934462/1.000772         
zip   32  999977 RabinKarp(seed=1, offs=0, map=ord, mult=0x8104225)   0/2/0.000116/1.000001           2/34/0.934462/0.998813         
zip   32  999977 RabinKarp(seed=0, offs=0, map=pow, mult=0xfffffffd)  0/2/0.000117/0.999999           2/35/0.934462/1.000780         
zip   32  999977 RabinKarp(seed=0, offs=0, map=pow, mult=0x41c64e6d)  0/2/0.000117/0.999999           2/36/0.934462/0.996362         
zip   32  999977 CyclicPoly(seed=0, offs=0, map=ipfs)                 0/2/0.000121/0.999991           1/37/0.934462/0.997189         
zip   32  999977 CyclicPoly(seed=0, offs=0, map=ord)                  0/2/0.000122/0.999989           1/35/0.934462/1.000225         
zip   32  999977 CyclicPoly(seed=0, offs=0, map=pow)                  0/2/0.000123/0.999987           1/35/0.934462/1.008489         
zip   32  999977 RabinKarp(seed=0, offs=0, map=mul, mult=0xfffffffd)  0/2/0.000123/0.999987           1/35/0.934462/1.004094         
zip   32  999977 RabinKarp(seed=0, offs=0, map=ord, mult=0xfffffffd)  0/2/0.000123/0.999987           1/36/0.934462/1.002365         
zip   32  999977 Gear(offs=0, map=ord)                                0/2/0.000123/0.999987           2/35/0.934462/1.002196         
zip   32  999977 Gear(offs=0, map=mul)                                0/2/0.000123/0.999987           3/35/0.934462/1.001046         
zip   32  999977 RabinKarp(seed=0, offs=0, map=pow, mult=0x8104225)   0/2/0.000124/0.999985           1/33/0.934462/0.995854         
zip   32  999977 CyclicPoly(seed=0, offs=0, map=mix)                  0/2/0.000125/0.999983           2/34/0.934462/1.005241         
zip   32  999977 RabinKarp(seed=0, offs=0, map=mul, mult=0x41c64e6d)  0/2/0.000126/0.999981           2/35/0.934462/1.001365         
zip   32  999977 RabinKarp(seed=0, offs=0, map=ord, mult=0x41c64e6d)  0/2/0.000126/0.999981           1/35/0.934462/0.993636         
zip   32  999977 CyclicPoly(seed=0, offs=0, map=mul)                  0/2/0.000130/0.999973           2/33/0.934462/0.991632         
zip   32  999977 Gear(offs=0, map=ipfs)                               0/3/0.000132/0.999967           2/36/0.934462/0.997470         
zip   32  999977 RollSum(seed=1, offs=0, map=pow, base=0x10000)       0/2/0.000141/0.999951           1/34/0.934462/0.998384         
zip   32  999977 RollSum(seed=1, offs=0, map=mul, base=0x10000)       0/4/0.022143/0.957007           0/86/0.960492/0.038885         
zip   32  999977 RollSum(seed=1, offs=0, map=ord, base=0x10000)       0/4/0.022143/0.957007           0/998/0.995881/0.001603        
zip   32  999977 RollSum(seed=0, offs=31, map=ord, base=0x10000)      0/4/0.022143/0.957007           0/990/0.995886/0.001603        
zip   1K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0x55555555)  0/2/0.000096/1.000041           2/35/0.934464/1.001445         
zip   1K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0x8104225)   0/2/0.000105/1.000023           2/33/0.934464/1.001981         
zip   1K 1000000 CyclicPoly(seed=0, offs=0, map=mix)                  0/2/0.000116/1.000001           2/36/0.934464/1.002079         
zip   1K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0xfffffffd)  0/2/0.000116/1.000001           1/34/0.934464/0.990473         
zip   1K 1000000 RabinKarp(seed=1, offs=0, map=ord, mult=0x8104225)   0/2/0.000120/0.999993           2/37/0.934464/0.999843         
zip   1K 1000000 RabinKarp(seed=0, offs=1, map=ord, mult=0x8104225)   0/2/0.000120/0.999993           3/36/0.934464/0.999703         
zip   1K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0x8104225)   0/2/0.000120/0.999993           3/36/0.934464/0.999703         
zip   1K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0x8104225)   0/2/0.000120/0.999993           3/35/0.934464/0.995488         
zip   1K 1000000 CyclicPoly(seed=0, offs=0, map=pow)                  0/2/0.000122/0.999989           1/34/0.934464/0.997306         
zip   1K 1000000 CyclicPoly(seed=0, offs=0, map=mul)                  0/2/0.000125/0.999983           2/36/0.934464/1.000808         
zip   1K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0x41c64e6d)  0/2/0.000126/0.999981           2/34/0.934464/1.002001         
zip   1K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0x41c64e6d)  0/2/0.000126/0.999981           3/37/0.934464/1.001602         
zip   1K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0x55555555)  0/2/0.000128/0.999977           2/36/0.934464/1.011520         
zip   1K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0x41c64e6d)  0/2/0.000128/0.999977           3/34/0.934464/1.009631         
zip   1K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0x55555555)  0/2/0.000128/0.999977           3/34/0.934464/1.001377         
zip   1K 1000000 CyclicPoly(seed=0, offs=0, map=ipfs)                 0/2/0.000130/0.999973           3/33/0.934464/0.998689         
zip   1K 1000000 CyclicPoly(seed=0, offs=0, map=ord)                  0/2/0.000136/0.999961           2/39/0.934464/0.995125         
zip   1K 1000000 RollSum(seed=1, offs=0, map=pow, base=0x10000)       0/2/0.000138/0.999957           1/32/0.934464/0.994070         
zip   1K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0xfffffffd)  0/2/0.000141/0.999951           2/36/0.934464/0.997513         
zip   1K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0xfffffffd)  0/2/0.000141/0.999951           2/34/0.934464/0.996331         
zip   1K 1000000 RollSum(seed=1, offs=0, map=mul, base=0x10000)       0/3/0.000641/0.998950           0/48/0.944123/0.118251         
zip   1K 1000000 RollSum(seed=0, offs=31, map=ord, base=0x10000)      0/3/0.000641/0.998950           0/166/0.967608/0.013592        
zip   1K 1000000 RollSum(seed=1, offs=0, map=ord, base=0x10000)       0/3/0.000641/0.998950           0/168/0.967617/0.013589        
zip   4K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0xfffffffd)  0/2/0.000093/1.000047           2/35/0.934464/1.010463         
zip   4K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0xfffffffd)  0/2/0.000093/1.000047           3/33/0.934464/1.003378         
zip   4K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0x41c64e6d)  0/2/0.000101/1.000031           2/35/0.934464/0.996603         
zip   4K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0x8104225)   0/2/0.000103/1.000027           2/36/0.934464/0.999048         
zip   4K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0x55555555)  0/2/0.000103/1.000027           2/34/0.934464/0.998789         
zip   4K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0x8104225)   0/2/0.000108/1.000017           2/35/0.934464/1.006915         
zip   4K 1000000 CyclicPoly(seed=0, offs=0, map=mix)                  0/2/0.000108/1.000017           2/34/0.934464/1.005892         
zip   4K 1000000 RabinKarp(seed=0, offs=1, map=ord, mult=0x8104225)   0/2/0.000108/1.000017           3/34/0.934464/0.996845         
zip   4K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0x8104225)   0/2/0.000108/1.000017           3/34/0.934464/0.996845         
zip   4K 1000000 RabinKarp(seed=1, offs=0, map=ord, mult=0x8104225)   0/2/0.000108/1.000017           2/34/0.934464/0.994806         
zip   4K 1000000 RollSum(seed=1, offs=0, map=pow, base=0x10000)       0/2/0.000115/1.000003           2/36/0.934464/0.998619         
zip   4K 1000000 CyclicPoly(seed=0, offs=0, map=pow)                  0/2/0.000117/0.999999           1/34/0.934464/1.008377         
zip   4K 1000000 CyclicPoly(seed=0, offs=0, map=mul)                  0/2/0.000119/0.999995           2/35/0.934464/0.996211         
zip   4K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0x41c64e6d)  0/2/0.000122/0.999989           3/36/0.934464/1.000563         
zip   4K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0x55555555)  0/2/0.000122/0.999989           2/34/0.934464/1.000513         
zip   4K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0x41c64e6d)  0/2/0.000122/0.999989           3/34/0.934464/1.000029         
zip   4K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0x55555555)  0/2/0.000122/0.999989           2/33/0.934464/0.984555         
zip   4K 1000000 CyclicPoly(seed=0, offs=0, map=ord)                  0/2/0.000123/0.999987           2/34/0.934464/1.004871         
zip   4K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0xfffffffd)  0/2/0.000125/0.999983           2/33/0.934464/0.997858         
zip   4K 1000000 CyclicPoly(seed=0, offs=0, map=ipfs)                 0/2/0.000126/0.999981           2/34/0.934464/0.998683         
zip   4K 1000000 RollSum(seed=1, offs=0, map=mul, base=0x10000)       0/2/0.000291/0.999651           0/46/0.934959/0.194340         
zip   4K 1000000 RollSum(seed=0, offs=31, map=ord, base=0x10000)      0/2/0.000291/0.999651           0/90/0.939478/0.043587         
zip   4K 1000000 RollSum(seed=1, offs=0, map=ord, base=0x10000)       0/2/0.000291/0.999651           0/86/0.939497/0.043581         
zip  16K 1000000 RollSum(seed=1, offs=0, map=pow, base=0x10000)       0/2/0.000101/1.000031           2/38/0.934464/1.003932         
zip  16K 1000000 CyclicPoly(seed=0, offs=0, map=ord)                  0/2/0.000104/1.000025           2/36/0.934464/1.002401         
zip  16K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0x55555555)  0/2/0.000108/1.000017           2/34/0.934464/1.003928         
zip  16K 1000000 CyclicPoly(seed=0, offs=0, map=pow)                  0/2/0.000110/1.000013           2/32/0.934464/0.999691         
zip  16K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0x41c64e6d)  0/2/0.000110/1.000013           2/32/0.934464/0.998779         
zip  16K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0x41c64e6d)  0/2/0.000110/1.000013           1/37/0.934464/0.992624         
zip  16K 1000000 CyclicPoly(seed=0, offs=0, map=mix)                  0/2/0.000115/1.000003           2/34/0.934464/0.996559         
zip  16K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0xfffffffd)  0/2/0.000116/1.000001           2/34/0.934464/1.001698         
zip  16K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0xfffffffd)  0/2/0.000116/1.000001           2/33/0.934464/0.987351         
zip  16K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0x55555555)  0/2/0.000120/0.999993           2/33/0.934464/1.000213         
zip  16K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0x55555555)  0/2/0.000120/0.999993           2/37/0.934464/0.998174         
zip  16K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0xfffffffd)  0/2/0.000122/0.999989           2/35/0.934464/0.995759         
zip  16K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0x8104225)   0/2/0.000124/0.999985           1/34/0.934464/1.007797         
zip  16K 1000000 CyclicPoly(seed=0, offs=0, map=ipfs)                 0/2/0.000125/0.999983           1/33/0.934464/0.993942         
zip  16K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0x41c64e6d)  0/2/0.000126/0.999981           2/34/0.934464/0.993857         
zip  16K 1000000 CyclicPoly(seed=0, offs=0, map=mul)                  0/2/0.000127/0.999979           2/36/0.934464/1.001291         
zip  16K 1000000 RollSum(seed=1, offs=0, map=mul, base=0x10000)       0/2/0.000127/0.999979           1/36/0.934464/0.798807         
zip  16K 1000000 RollSum(seed=0, offs=31, map=ord, base=0x10000)      0/2/0.000127/0.999979           1/44/0.934464/0.416684         
zip  16K 1000000 RollSum(seed=1, offs=0, map=ord, base=0x10000)       0/2/0.000127/0.999979           0/47/0.934465/0.416395         
zip  16K 1000000 RabinKarp(seed=1, offs=0, map=ord, mult=0x8104225)   0/2/0.000131/0.999971           2/35/0.934464/1.007661         
zip  16K 1000000 RabinKarp(seed=0, offs=1, map=ord, mult=0x8104225)   0/2/0.000131/0.999971           3/34/0.934464/1.004794         
zip  16K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0x8104225)   0/2/0.000131/0.999971           3/34/0.934464/1.004794         
zip  16K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0x8104225)   0/2/0.000131/0.999971           2/35/0.934464/1.004410         
zip  64K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0x41c64e6d)  0/2/0.000102/1.000029           2/33/0.934464/1.013298         
zip  64K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0x41c64e6d)  0/2/0.000102/1.000029           2/36/0.934464/1.003147         
zip  64K 1000000 RollSum(seed=1, offs=0, map=mul, base=0x10000)       0/2/0.000105/1.000023           2/37/0.934464/0.896147         
zip  64K 1000000 RollSum(seed=0, offs=31, map=ord, base=0x10000)      0/2/0.000105/1.000023           1/46/0.934464/0.523195         
zip  64K 1000000 RollSum(seed=1, offs=0, map=ord, base=0x10000)       0/2/0.000105/1.000023           1/44/0.934464/0.522998         
zip  64K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0x41c64e6d)  0/2/0.000107/1.000019           3/34/0.934464/1.000391         
zip  64K 1000000 CyclicPoly(seed=0, offs=0, map=ipfs)                 0/2/0.000107/1.000019           2/36/0.934464/0.994842         
zip  64K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0xfffffffd)  0/2/0.000108/1.000017           2/33/0.934464/0.997969         
zip  64K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0x55555555)  0/2/0.000109/1.000015           2/35/0.934464/1.001441         
zip  64K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0x55555555)  0/2/0.000109/1.000015           2/34/0.934464/1.000051         
zip  64K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0xfffffffd)  0/2/0.000110/1.000013           2/34/0.934464/1.007284         
zip  64K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0xfffffffd)  0/2/0.000110/1.000013           0/37/0.934465/0.994911         
zip  64K 1000000 CyclicPoly(seed=0, offs=0, map=mix)                  0/2/0.000112/1.000009           3/34/0.934464/1.006702         
zip  64K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0x55555555)  0/2/0.000114/1.000005           2/34/0.934464/1.006001         
zip  64K 1000000 RabinKarp(seed=0, offs=0, map=pow, mult=0x8104225)   0/2/0.000115/1.000003           2/33/0.934464/1.001545         
zip  64K 1000000 CyclicPoly(seed=0, offs=0, map=ord)                  0/2/0.000115/1.000003           2/34/0.934464/0.996136         
zip  64K 1000000 CyclicPoly(seed=0, offs=0, map=pow)                  0/2/0.000116/1.000001           2/33/0.934464/1.001201         
zip  64K 1000000 RabinKarp(seed=0, offs=1, map=ord, mult=0x8104225)   0/2/0.000119/0.999995           2/34/0.934464/1.006068         
zip  64K 1000000 RabinKarp(seed=0, offs=0, map=ord, mult=0x8104225)   0/2/0.000119/0.999995           2/34/0.934464/1.006068         
zip  64K 1000000 RabinKarp(seed=1, offs=0, map=ord, mult=0x8104225)   0/2/0.000119/0.999995           2/36/0.934464/1.001917         
zip  64K 1000000 RabinKarp(seed=0, offs=0, map=mul, mult=0x8104225)   0/2/0.000119/0.999995           2/38/0.934464/0.994731         
zip  64K 1000000 RollSum(seed=1, offs=0, map=pow, base=0x10000)       0/2/0.000122/0.999989           2/35/0.934464/0.995151         
zip  64K 1000000 CyclicPoly(seed=0, offs=0, map=mul)                  0/2/0.000130/0.999973           3/33/0.934464/1.000740         
=== ==== ======= ==================================================== =========================       =========================      
