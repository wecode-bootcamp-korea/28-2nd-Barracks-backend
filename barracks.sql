-- MySQL dump 10.13  Distrib 8.0.27, for macos11.6 (x86_64)
--
-- Host: localhost    Database: barracks
-- ------------------------------------------------------
-- Server version	8.0.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comments` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `content` varchar(350) COLLATE utf8mb4_general_ci NOT NULL,
  `posting_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `comments_posting_id_75a1ee6d_fk_postings_id` (`posting_id`),
  KEY `comments_user_id_b8fd0b64_fk_users_id` (`user_id`),
  CONSTRAINT `comments_posting_id_75a1ee6d_fk_postings_id` FOREIGN KEY (`posting_id`) REFERENCES `postings` (`id`),
  CONSTRAINT `comments_user_id_b8fd0b64_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'contenttypes','contenttype'),(11,'postings','comment'),(10,'postings','image'),(9,'postings','like'),(8,'postings','posting'),(4,'postings','residence'),(5,'postings','size'),(6,'postings','space'),(7,'postings','style'),(2,'sessions','session'),(3,'users','user');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2022-01-20 10:07:29.737549'),(2,'contenttypes','0002_remove_content_type_name','2022-01-20 10:07:29.765154'),(3,'users','0001_initial','2022-01-20 10:07:29.775479'),(4,'postings','0001_initial','2022-01-20 10:07:30.031587'),(5,'postings','0002_alter_residence_table_alter_size_table_and_more','2022-01-20 10:07:30.072551'),(6,'postings','0003_remove_posting_name_posting_title_and_more','2022-01-20 10:07:30.213689'),(7,'sessions','0001_initial','2022-01-20 10:07:30.227667');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_general_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `images`
--

DROP TABLE IF EXISTS `images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `images` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image_url` varchar(2000) COLLATE utf8mb4_general_ci NOT NULL,
  `posting_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `images_posting_id_3fe5e905_fk_postings_id` (`posting_id`),
  CONSTRAINT `images_posting_id_3fe5e905_fk_postings_id` FOREIGN KEY (`posting_id`) REFERENCES `postings` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `images`
--

LOCK TABLES `images` WRITE;
/*!40000 ALTER TABLE `images` DISABLE KEYS */;
INSERT INTO `images` VALUES (1,'https://cdn.pixabay.com/photo/2016/11/18/17/20/living-room-1835923_1280.jpg',1),(2,'https://cdn.pixabay.com/photo/2014/08/11/21/39/wall-416060_1280.jpg',1),(3,'https://cdn.pixabay.com/photo/2015/10/20/18/57/furniture-998265_1280.jpg',1),(4,'https://cdn.pixabay.com/photo/2016/06/24/10/47/house-1477041_1280.jpg',1),(5,'https://cdn.pixabay.com/photo/2017/09/09/18/25/living-room-2732939_1280.jpg',2),(6,'https://cdn.pixabay.com/photo/2017/03/22/17/39/kitchen-2165756_1280.jpg',2),(7,'https://cdn.pixabay.com/photo/2017/08/27/10/16/interior-2685521_1280.jpg',2),(8,'https://cdn.pixabay.com/photo/2014/12/27/14/37/living-room-581073_1280.jpg',2),(9,'https://cdn.pixabay.com/photo/2014/08/11/21/40/bedroom-416062_1280.jpg',3),(10,'https://cdn.pixabay.com/photo/2017/03/28/12/11/chairs-2181960_1280.jpg',3),(11,'https://cdn.pixabay.com/photo/2017/01/07/17/48/interior-1961070_1280.jpg',3),(12,'https://cdn.pixabay.com/photo/2015/04/20/06/46/office-730681_1280.jpg',7),(13,'https://cdn.pixabay.com/photo/2016/11/18/14/05/brick-wall-1834784_1280.jpg',7),(14,'https://cdn.pixabay.com/photo/2017/03/28/12/10/chairs-2181947_1280.jpg',7),(15,'https://cdn.pixabay.com/photo/2016/04/18/08/50/kitchen-1336160_1280.jpg',8),(16,'https://cdn.pixabay.com/photo/2017/03/19/01/43/living-room-2155376_1280.jpg',8),(17,'https://cdn.pixabay.com/photo/2016/08/26/15/06/home-1622401_1280.jpg',8),(18,'https://cdn.pixabay.com/photo/2017/08/02/01/01/living-room-2569325_1280.jpg',9),(19,'https://cdn.pixabay.com/photo/2016/12/30/07/59/kitchen-1940174_1280.jpg',9),(20,'https://cdn.pixabay.com/photo/2017/03/28/12/17/chairs-2181994_1280.jpg',10),(21,'https://cdn.pixabay.com/photo/2014/09/15/21/46/couch-447484_1280.jpg',10),(22,'https://cdn.pixabay.com/photo/2017/08/03/15/38/architecture-2576906_1280.jpg',10),(23,'https://cdn.pixabay.com/photo/2018/01/26/08/15/dining-room-3108037_1280.jpg',11),(24,'https://cdn.pixabay.com/photo/2020/11/24/11/36/bedroom-5772286_1280.jpg',11),(25,'https://cdn.pixabay.com/photo/2020/10/18/09/16/bedroom-5664221_1280.jpg',12),(26,'https://cdn.pixabay.com/photo/2016/09/22/11/55/kitchen-1687121_1280.jpg',12),(27,'https://cdn.pixabay.com/photo/2017/06/13/22/42/kitchen-2400367_1280.jpg',13),(28,'https://cdn.pixabay.com/photo/2016/11/19/13/06/bed-1839183_1280.jpg',13),(29,'https://cdn.pixabay.com/photo/2021/11/08/00/30/bedroom-6778193_1280.jpg',14),(30,'https://cdn.pixabay.com/photo/2016/03/28/09/34/bedroom-1285156_1280.jpg',14);
/*!40000 ALTER TABLE `images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `likes`
--

DROP TABLE IF EXISTS `likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `likes` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `is_like` tinyint(1) NOT NULL,
  `posting_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `likes_posting_id_aebe0074_fk_postings_id` (`posting_id`),
  KEY `likes_user_id_0899754c_fk_users_id` (`user_id`),
  CONSTRAINT `likes_posting_id_aebe0074_fk_postings_id` FOREIGN KEY (`posting_id`) REFERENCES `postings` (`id`),
  CONSTRAINT `likes_user_id_0899754c_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `likes`
--

LOCK TABLES `likes` WRITE;
/*!40000 ALTER TABLE `likes` DISABLE KEYS */;
/*!40000 ALTER TABLE `likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `postings`
--

DROP TABLE IF EXISTS `postings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `postings` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `tags` varchar(300) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `content` longtext COLLATE utf8mb4_general_ci,
  `hits` int NOT NULL,
  `residence_id` bigint DEFAULT NULL,
  `size_id` bigint DEFAULT NULL,
  `space_id` bigint NOT NULL,
  `style_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL,
  `title` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `postings_residence_id_3e384839_fk_postings_residence_id` (`residence_id`),
  KEY `postings_size_id_ce74af55_fk_postings_size_id` (`size_id`),
  KEY `postings_space_id_3fffcdb9_fk_postings_space_id` (`space_id`),
  KEY `postings_style_id_13af41b3_fk_postings_style_id` (`style_id`),
  KEY `postings_user_id_86e05dd0_fk_users_id` (`user_id`),
  CONSTRAINT `postings_residence_id_3e384839_fk_postings_residence_id` FOREIGN KEY (`residence_id`) REFERENCES `residences` (`id`),
  CONSTRAINT `postings_size_id_ce74af55_fk_postings_size_id` FOREIGN KEY (`size_id`) REFERENCES `sizes` (`id`),
  CONSTRAINT `postings_space_id_3fffcdb9_fk_postings_space_id` FOREIGN KEY (`space_id`) REFERENCES `spaces` (`id`),
  CONSTRAINT `postings_style_id_13af41b3_fk_postings_style_id` FOREIGN KEY (`style_id`) REFERENCES `styles` (`id`),
  CONSTRAINT `postings_user_id_86e05dd0_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `postings`
--

LOCK TABLES `postings` WRITE;
/*!40000 ALTER TABLE `postings` DISABLE KEYS */;
INSERT INTO `postings` VALUES (1,'2022-01-20 10:16:27.125727','2022-01-20 10:16:27.126064','#짱,#최고','어떤가요 제 인테리어~~?',0,2,2,1,3,1,'오래된 우리집 짱이지롱'),(2,'2022-01-20 10:16:27.134440','2022-01-20 10:16:27.134473','#히히','이거 좀 돈지랄인가^^',0,NULL,1,1,2,1,'가난한 학생의 집'),(3,'2022-01-20 10:16:27.136186','2022-01-20 10:16:27.136217','#감성,#인테리어','돈을 퍼부어서 꾸며보았습니다.',0,2,3,1,3,1,'이쁜 인테리어의 거실'),(4,'2022-01-20 10:16:27.143464','2022-01-20 10:16:27.143505','','따스한 침실을 구경해보셔요!',0,1,3,2,1,1,'따스한 온기가 느껴지는 침실'),(5,'2022-01-20 10:16:27.145481','2022-01-20 10:16:27.145510','#원룸,#자취방','인테리어 따위 신경쓰지 않았어요.',0,1,1,1,1,1,'나에게 집은 잠만 자면 되는 곳'),(6,'2022-01-20 10:16:27.147322','2022-01-20 10:16:27.147349','#동기생활관,#군대','여기 있기 싫다.',0,NULL,1,3,2,1,'내무반이 생각나는 공간'),(7,'2022-01-20 10:16:27.148941','2022-01-20 10:16:27.148965','#놀러오삼','짱이지~~?',0,3,3,1,3,1,'우리 집에 놀러와요'),(8,'2022-01-20 10:16:27.150306','2022-01-20 10:16:27.150328','#한옥','경복궁이야 집이야?',0,3,3,3,3,1,'전통가옥을 떠올리는 공간'),(9,'2022-01-20 10:16:27.151818','2022-01-20 10:16:27.151844','#놀러와','짱이지~~ ㅋㅋㅋㅋㅋ',0,NULL,1,1,2,1,'최고다'),(10,'2022-01-20 10:16:27.153118','2022-01-20 10:16:27.153150','','따끈따근한 우리집',0,2,NULL,2,2,1,'우리집은 추워'),(11,'2022-01-20 10:16:27.154218','2022-01-20 10:16:27.154242','#심플,#거실꾸미기,#거실인테리어,#홈카페','유럽 무드로 30평대 신축을 홈카페로 꾸며봤습니다~',0,3,2,1,3,1,'유럽 무드를 담은 따끈따끈 30평대 신축 ft. 홈카페'),(12,'2022-01-20 10:16:27.155545','2022-01-20 10:16:27.155565','#원룸,#자취방,#복층','저도 원룸 꾸며봤씁니다~',0,2,1,2,1,1,'하늘 액자 같은 통창뷰! 원목 가득한 코지st 원룸'),(13,'2022-01-20 10:16:27.156422','2022-01-20 10:16:27.156441','','ㅋㅋㅋㅋ이쁘져?',0,2,1,3,1,1,'러블리 그 자체, 빈티지가 담긴 앤티크 투룸 전셋집'),(14,'2022-01-20 10:16:27.158358','2022-01-20 10:16:27.158379','#거실,#주방','저희 집 짱이죠?',0,1,1,1,1,1,'길쭉한 모양의 5평 원룸을 침실-거실-주방으로'),(15,'2022-01-20 10:16:27.159188','2022-01-20 10:16:27.159208','#옷장,#원목옷장,#원목행거,#원목가구,#우드인테리어,#라이크노아,#빈티지조명,#드엘리사,#빈티지램프,#우드램프,#침실','짱입니다!!!',0,2,3,2,2,1,'집안 곳곳 우드로 아늑하게, 20평대 신혼집 스타일링'),(16,'2022-01-20 10:16:27.159913','2022-01-20 10:16:27.159932','','히히 우리집입니댜',0,3,2,3,1,1,'내력벽을 아치게이트로! 시공 포인트가 있는 구축 신혼집'),(17,'2022-01-20 10:16:27.160711','2022-01-20 10:16:27.160733','#침대,#안방,#안방인테리어,#호텔침대','잠만 잘 수 있음 된다',0,3,1,1,1,1,'매일이 호캉스~ 호텔 같이 깔끔한 30평대 리모델링'),(18,'2022-01-20 10:16:27.161612','2022-01-20 10:16:27.161638','#쿄쿄','캬캬캬',0,3,3,2,2,1,'부모님집을 스튜디오로, 사계절이 아름다운 로망집'),(19,'2022-01-20 10:16:27.162563','2022-01-20 10:16:27.162586','','크크크',0,1,2,3,1,1,'여행을 위해 일상을 꾸리는, 디자이너의 따스한 원룸'),(20,'2022-01-20 10:16:27.163372','2022-01-20 10:16:27.163391','#안방,#침실,#안방인테리어,#레트로,#미드센츄리모던','히히히',0,1,NULL,1,1,1,'미드센추리 모던 느낌을 더한 싱글 하우스 리모델링'),(21,'2022-01-20 10:16:27.164140','2022-01-20 10:16:27.164159','#싱글라이프','호호',0,1,2,1,1,1,'20년된 복층 원룸, 화이트 리모델링'),(22,'2022-01-20 10:16:27.165442','2022-01-20 10:16:27.165460','#신혼부부','집 짱',0,2,3,2,1,1,'개성과 편안함의 균형이 잡힌 집'),(23,'2022-01-20 10:16:27.166680','2022-01-20 10:16:27.166699','#취학자녀와 함께','오늘의 집 사이트 망해라',0,2,1,2,3,1,'창문을 열면 새소리도 들리는, 저층의 매력'),(24,'2022-01-20 10:16:27.167440','2022-01-20 10:16:27.167459','#신혼부부','오늘의집 비싸게 파는듯',0,NULL,2,1,2,1,'크리스마스 데코와 셀프 시공으로 매주 변하는 집'),(25,'2022-01-20 10:16:27.168826','2022-01-20 10:16:27.168850','#단독주택','우리집 이쁘지?',0,1,2,2,2,1,'하루를 나누고 맛있는 걸 먹는 기쁨이 있는 우리들의 집'),(26,'2022-01-20 10:16:27.169742','2022-01-20 10:16:27.169769','#신혼부부','구경 오세요',0,2,3,3,1,1,'따뜻하고 단정한 첫 신혼집, 24평 복도식 아파트'),(27,'2022-01-20 10:16:27.170709','2022-01-20 10:16:27.170731','','집 꾸미기',0,2,1,3,3,1,'제품 디자이너의 안목이 담긴 미니 스튜디오st 작은 방'),(28,'2022-01-20 10:16:27.172064','2022-01-20 10:16:27.172083','#코지','30평대 코어 하우스로~',0,1,1,3,3,1,'우드의 내추럴함과 태슬로 완성한 30평대 코지 하우스'),(29,'2022-01-20 10:16:27.172930','2022-01-20 10:16:27.172949','#코지,#원룸','코지 스타일 원룸 꾸미기',0,3,2,2,1,1,'하늘 액자 같은 통창뷰! 원목 가득한 코지st 원룸'),(30,'2022-01-20 10:16:27.173650','2022-01-20 10:16:27.173669','#거실,#최고','리모델링 다시 했어요~',0,3,1,3,1,1,'거실에 숲이 들어왔어요! 네 식구에게 꼭 맞춘 리모델링');
/*!40000 ALTER TABLE `postings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `residences`
--

DROP TABLE IF EXISTS `residences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `residences` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `residences`
--

LOCK TABLES `residences` WRITE;
/*!40000 ALTER TABLE `residences` DISABLE KEYS */;
INSERT INTO `residences` VALUES (1,'오피스텔'),(2,'아파트'),(3,'빌라');
/*!40000 ALTER TABLE `residences` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sizes`
--

DROP TABLE IF EXISTS `sizes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sizes` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sizes`
--

LOCK TABLES `sizes` WRITE;
/*!40000 ALTER TABLE `sizes` DISABLE KEYS */;
INSERT INTO `sizes` VALUES (1,'10평 대'),(2,'20평 대'),(3,'30평 대');
/*!40000 ALTER TABLE `sizes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `spaces`
--

DROP TABLE IF EXISTS `spaces`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `spaces` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spaces`
--

LOCK TABLES `spaces` WRITE;
/*!40000 ALTER TABLE `spaces` DISABLE KEYS */;
INSERT INTO `spaces` VALUES (1,'거실'),(2,'침실'),(3,'욕실');
/*!40000 ALTER TABLE `spaces` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `styles`
--

DROP TABLE IF EXISTS `styles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `styles` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `styles`
--

LOCK TABLES `styles` WRITE;
/*!40000 ALTER TABLE `styles` DISABLE KEYS */;
INSERT INTO `styles` VALUES (1,'모던'),(2,'빈티지'),(3,'내추럴');
/*!40000 ALTER TABLE `styles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `kakao_id` int NOT NULL,
  `email` varchar(150) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nickname` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `profile_image_url` varchar(2000) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `kakao_id` (`kakao_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'2022-01-20 10:13:34.294974','2022-01-20 10:13:34.295018',2074410349,'dkdud2408@kakao.com','아영','http://k.kakaocdn.net/dn/bQpvV5/btrp8qGq28a/uaHemjFTr9t58sqvn9YYAK/img_640x640.jpg');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-01-20 19:22:31
