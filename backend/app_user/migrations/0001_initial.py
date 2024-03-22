# Generated by Django 4.1.3 on 2024-03-17 09:10

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('app_item', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('username', models.CharField(default=uuid.uuid4, max_length=100, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()])),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Người dùng',
                'db_table': 'tb_user',
            },
        ),
        migrations.CreateModel(
            name='Characters',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('gender', models.CharField(choices=[('1', 'Nam'), ('2', 'Nữ')], max_length=10)),
                ('appearance', models.ImageField(blank=True, default='temp/avatar.png', null=True, upload_to='appearance')),
                ('date_join', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Nhân vật',
                'db_table': 'tb_characters',
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(default='')),
            ],
            options={
                'verbose_name': 'Danh hiệu',
                'db_table': 'tb_title',
            },
        ),
        migrations.CreateModel(
            name='StudyProcess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process', models.IntegerField(default=0)),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='StudyProcess_book', to='app_item.book')),
                ('char', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='StudyProcess_characters', to='app_user.characters')),
            ],
            options={
                'verbose_name': 'Lĩnh ngộ công pháp',
                'db_table': 'tb_study_process',
            },
        ),
        migrations.CreateModel(
            name='Study',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ManyToManyField(blank=True, related_name='Study_book', to='app_item.book')),
                ('char', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Study_characters', to='app_user.characters')),
            ],
            options={
                'verbose_name': 'Công pháp lĩnh ngộ',
                'db_table': 'tb_study',
            },
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.IntegerField(default=0)),
                ('char1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Relationship_char1', to='app_user.characters')),
                ('char2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Relationship_char2', to='app_user.characters')),
            ],
            options={
                'verbose_name': 'Mối quan hệ',
                'db_table': 'tb_relationship',
            },
        ),
        migrations.CreateModel(
            name='Properties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('canh_gioi', models.IntegerField(default=1)),
                ('linh_luc', models.IntegerField(default=0)),
                ('linh_luc_yeu_cau', models.IntegerField(default=100)),
                ('tuoi', models.IntegerField(default=1, verbose_name='tuổi')),
                ('tuoi_tho', models.IntegerField(default=80, verbose_name='tuổi thọ')),
                ('tam_tinh', models.IntegerField(default=10, verbose_name='tâm tình')),
                ('suc_khoe', models.IntegerField(default=10, verbose_name='sức khỏe')),
                ('mau_huyet', models.IntegerField(default=100, verbose_name='máu huyết')),
                ('cong_kich', models.IntegerField(default=10, verbose_name='công kích')),
                ('phong_ngu', models.IntegerField(default=1, verbose_name='phòng ngự')),
                ('toc_do', models.IntegerField(default=1, verbose_name='tốc độ')),
                ('hoa_thuoc_tinh', models.IntegerField(default=0, verbose_name='hỏa thuộc tính')),
                ('thuy_thuoc_tinh', models.IntegerField(default=0, verbose_name='thủy thuộc tính')),
                ('kim_thuoc_tinh', models.IntegerField(default=0, verbose_name='kim thuộc tính')),
                ('moc_thuoc_tinh', models.IntegerField(default=0, verbose_name='mộc thuộc tính')),
                ('tho_thuoc_tinh', models.IntegerField(default=0, verbose_name='thổ thuộc tính')),
                ('luyen_khi', models.IntegerField(default=0, verbose_name='luyện khí')),
                ('luyen_dan', models.IntegerField(default=0, verbose_name='luyện đan')),
                ('duoc_lieu', models.IntegerField(default=0, verbose_name='dược liệu')),
                ('khoang_san', models.IntegerField(default=0, verbose_name='khoáng sản')),
                ('may_man', models.IntegerField(default=0, verbose_name='may mắn')),
                ('char', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Properties_characters', to='app_user.characters')),
            ],
            options={
                'verbose_name': 'Thuộc tính',
                'db_table': 'tb_properties',
            },
        ),
        migrations.CreateModel(
            name='OwnPet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(default=1)),
                ('exp', models.IntegerField(default=0)),
                ('char', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='OwnPet_char', to='app_user.characters')),
                ('pet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='OwnPet_pet', to='app_item.pet')),
            ],
            options={
                'verbose_name': 'Nuôi thú',
                'db_table': 'tb_own_pet',
            },
        ),
        migrations.CreateModel(
            name='OwnMaid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(default=1)),
                ('exp', models.IntegerField(default=0)),
                ('char', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='OwnMaid_char', to='app_user.characters')),
                ('maid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='OwnMaid_maid', to='app_item.maid')),
            ],
            options={
                'verbose_name': 'Nuôi người hầu',
                'db_table': 'tb_own_maid',
            },
        ),
        migrations.CreateModel(
            name='Money',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money', models.IntegerField(default=0)),
                ('dedication', models.IntegerField(default=0)),
                ('char', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Money_characters', to='app_user.characters')),
            ],
            options={
                'verbose_name': 'Tiền tệ',
                'db_table': 'tb_money',
            },
        ),
        migrations.CreateModel(
            name='Knowledge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('char', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Knowledge_char', to='app_user.characters')),
                ('menu', models.ManyToManyField(blank=True, related_name='Knowledge_menu', to='app_item.menu')),
            ],
            options={
                'verbose_name': 'Kiến thức',
                'db_table': 'tb_knowledge',
            },
        ),
        migrations.CreateModel(
            name='Equipped',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('char', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Equipped_characters', to='app_user.characters')),
                ('hand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Equipped_hand', to='app_item.item')),
                ('head', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Equipped_head', to='app_item.item')),
                ('shirt', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Equipped_shirt', to='app_item.item')),
                ('trousers', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Equipped_trousers', to='app_item.item')),
            ],
            options={
                'verbose_name': 'Trang bị',
                'db_table': 'tb_equipped',
            },
        ),
        migrations.AddField(
            model_name='characters',
            name='title',
            field=models.ManyToManyField(blank=True, related_name='Characters_title', to='app_user.title'),
        ),
        migrations.AddField(
            model_name='characters',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Characters_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Bag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.JSONField(default=dict)),
                ('books', models.JSONField(default=dict)),
                ('char', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Bag_characters', to='app_user.characters')),
            ],
            options={
                'verbose_name': 'Túi đồ',
                'db_table': 'tb_bag',
            },
        ),
    ]
