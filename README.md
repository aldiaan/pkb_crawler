# PKB Crawler

## Instalasi :
1. Pastikan anda mempunyai browser Google Chrome
2. Masukan chromedriver yang ada di ./pkb_crawler/drivers/windows untuk windows dan ./pkb_crawler/drivers/linux untuk linux:
    i. untuk linux copy chromedriver ke /usr/bin atau /usr/local/bin
    ii. untuk windows copy path chromedriver.exe ke Path system variable
3. Install package yang dibutuhkan crawler dengan command :
    i. `pip install selenium` (scrapping)
    ii. `pip install requests` (login instagram)

## Pemakaian
### Level 1
list parameter yang tersedia yang dapat dilihat dengan command `python pkb_crawler -h` :

```
-h, --help        show this help message and exit
-m , --mode       format untuk output tugas (level1), contoh : --mode 1
-u , --username   username untuk login instagram 
-p , --password   password untuk login instagram
--uid             instagram id user mula mula yang ingin di-crawl
-n , --limit      scrap n-posts dari setiap user (optional, default=Inf)
-r , --ring       mengambil follower sampai n-ring (default=1)
-c                melanjutkan dari scrapping sebelumnya (experimental)
```

untuk men-generate dataframe level 1 gunakan command :

`python pkb_crawler --username <username_ig_anda> --password <password_ig_anda> --uid <id_instagram_yang_ingin_dicrawl> --ring n --mode 1`

untuk melanjutkan crawling sebelumnya dapat digunakan command :
`python pkb_crawler --mode 1 -c`

hasil dari command tersebut adalah file dengan format .csv dan diletakan dalam folder `./project_pkb/pkb_crawler/data/tanggal_bulan_tahun_jam_menit_detik.csv`

### Level 2
program ini menghasilkan bag of pair words dari dataframe level 1

lokasi file level_2.py ada di `./pkb_crawler/level_2.py`
untuk men-generate dataframe level 2 gunakan command :
`python level_2.py --input <lokasi_csv_level_1> --output <lokasi_peletakan_csv_level_2>`

contoh penggunaan command level2 :
`python level_2.py --input K:\\pkb\\project_pkb\\pkb_crawler\\data\\05_10_2019_124135_level1_dump.csv --output K:\\pkb\\project_pkb\\pkb_crawler\\data\\05_10_2019_124135_level2_dump.csv`
