# faucet

> Licence: MIT Licence
> 
> Author: Bocheng Zhang
> 
> Language: Python (>= 3.6)

## What Is This

本程序主要用于private net，向输入地址转入指定数量的测试币。

## 如何使用

1. Run `pip install -r requirements.txt` to install dependencies
2. Transfer testcoin

```bash
python3 faucet.py -n did -t Ea8DpuVv4pmxyKuwatYbCD7fpCGpcq9prz -v 0.0011
```

## 参数说明

1. -n --node

输入需要操作的链为主链还是侧链，可选值为ela、did[默认值]

2. -t --to

输入收币地址

3. -v --value

输入期望转入的测试币数量