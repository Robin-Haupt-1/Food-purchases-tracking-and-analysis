
# What information should get stored (2022-02-04)

I want the store of purchase information be both very accurate (concrete) as well as easy to analyze and to derive higher-level insights from (abstract).
One challenge to that is the question of how to categorize items. For instance, there are many different brands of rolled oats, soy milk or lentils that you could buy at different stores in different package sizes, but the actual product is mostly the same, since these products are all commodities. In a monthly overview, i would rather know how many lentils i bought in total than see all the different brands and stores i got them from. Still it would be interesting to preserve store, brand and package size information as well.

That's why my plan is to create two types of product representation objects, one concrete and one abstract, and have every concrete one point to one and only one abstract one as it's 'base type', while specifying how large an amount of it it represents. Then when entering new purchases, you can choose from all the concrete products you've ever bought or create a new one. This saves the trouble of entering brand name and package size anew every time.

In the future i could add even higher-level categories like 'greens', 'frozen foods' or 'spices' that the abstract produce entities get tagged with. But there is no need to worry about this now, since the main focus needs to be on creating a means to accurately copy the information from all the receipts i am currently hoarding before their number gets discouragingly high.

## Product object layout

### Abstract product

#### Name 
Eg. dried red lentils, fresh kale, paprika spice powder

#### How is the amount measured

Usually in grams, but could also be milliliters for liquids or one bunch (for fresh parsley for example) or one piece of fruit or vegetable (one eggplant) though in instances of the last type in might be preferable to establish approximate weights and stick with those.

### Concrete product
 
#### Name
-> Inherited from base product

#### Brand
Brand name that's on the packaging

#### Measurement (weight/volume)
For anything that has a fixed package size


Note that price is not a piece of data to be stored in the product item's definition, since it can and will fluctuate. It is instead to be derived from the purchase history.


