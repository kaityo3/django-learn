from django.db import models



# Create your models here.

class BaseModel(models.Model):
    # インスタンス作成時に変更される
    create_at = models.DateTimeField(auto_now_add=True)
    # インスタンス保存時に変更される
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        # 抽象モデルとして定義
        abstract = True


# 商品の種類
class ProductTypes(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "product_types"

# 生産者
class Manufacturers(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "manufacturers"

# 商品
class Products(BaseModel):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    stock = models.IntegerField()
    # 商品の種類がなくなってもnullを入れる
    product_type = models.ForeignKey("ProductTypes", null=True, on_delete=models.SET_NULL)
    # 生産者がなくなれば、この製品も削除する
    manufacturer = models.ForeignKey("Manufacturers", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "products"

class ProductPictures(BaseModel):
    picture = models.FileField(upload_to="product_pictures/")
    # productがなくなれば、写真も削除する
    product = models.ForeignKey("Products", on_delete = models.CASCADE)
    # 順番を変更するためのフィールド
    order = models.IntegerField()

    class Meta:
        db_table = "product_pictures"
        # orderに合わせて昇順でソードされる
        ordering = ["order"]
    def __str__(self):
        return self.product.name + ":" + str(self.order)

class CartItemsManager(models.Manager):
    def save_item(self, product_id, quantity, cart):
        # ForeignKeyを使用した場合、リレーション先は"リレーションされたmodel_id"と登録されるため_idでも使用できる。
        c = self.model(quantity=quantity, product_id = product_id, cart = cart)
        c.save()
    
    def get_items(self, user_id):
        # cart_idとuser_idは1:1で紐づきあり
        query = self.model.filter(cart_id = user_id)
        return query

class CartItems(BaseModel):
    product = models.ForeignKey("Products", on_delete=models.CASCADE)
    # 正の値しか認めないfield
    quantity = models.PositiveIntegerField()
    cart = models.ForeignKey("Carts", on_delete=models.CASCADE)

    objects= CartItemsManager()

    class Meta:
        db_table = "cart_items"
        # productとcartは重複した値が入らないようにする。
        unique_together = [["product", "cart"]]
    
    def __str__(self):
        return self.product.name + ":" + str(self.quantity)

class Carts(BaseModel):
    user = models.OneToOneField(
        # from accounts import Usersをして Users,と指定することも可能
        "accounts.Users",
        on_delete = models.CASCADE,
        primary_key = True,
    )
    class Meta:
        db_table = "carts"

    def __str__(self):
        return self.user.name + " cart" 

    
