import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(page_title="📖 Biblia App", page_icon="✝️", layout="wide")

# ==========================================
# BASE DE DATOS
# ==========================================
@st.cache_resource
def init_data():
    conn = sqlite3.connect("biblia.db")
    c = conn.cursor()
    
    # Libros
    c.execute("""CREATE TABLE IF NOT EXISTS libros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        testamento TEXT,
        autor TEXT,
        fecha TEXT,
        lugar_escritura TEXT,
        lugar_exacto TEXT,
        temas TEXT
    )""")
    
    # Verificar si ya hay datos
    c.execute("SELECT COUNT(*) FROM libros")
    if c.fetchone()[0] == 0:
        libros = [
            ("Génesis", "Antiguo Testamento", "Moisés", "1445-1405 a.C.", "Desierto de Sinaí", "Monte Sinaí", "Creación, Patriarcas"),
            ("Éxodo", "Antiguo Testamento", "Moisés", "1445-1405 a.C.", "Desierto de Sinaí", "Monte Sinaí", "Éxodo, Ley"),
            ("Deuteronomio", "Antiguo Testamento", "Moisés", "1405 a.C.", "Moab", "Llanuras de Moab", "Segunda Ley"),
            ("Salmo", "Antiguo Testamento", "David y otros", "~1000-500 a.C.", "Jerusalén", "Jerusalén", "Alabanza, Oración"),
            ("Proverbios", "Antiguo Testamento", "Salomón", "~950 a.C.", "Jerusalén", "Jerusalén", "Sabiduría"),
            ("Isaías", "Antiguo Testamento", "Isaías", "740-680 a.C.", "Judá", "Jerusalén", "Profecías, Mesías"),
            ("Jeremías", "Antiguo Testamento", "Jeremías", "626-586 a.C.", "Judá", "Jerusalén", "Juicio, Esperanza"),
            ("Mateo", "Nuevo Testamento", "Mateo", "50-70 d.C.", "Siria", "Antioquía", "Jesús, Reino"),
            ("Marcos", "Nuevo Testamento", "Juan Marcos", "50-70 d.C.", "Roma", "Roma", "Jesús, Siervo"),
            ("Lucas", "Nuevo Testamento", "Lucas", "60-80 d.C.", "Grecia", "Aquea", "Jesús, Compasión"),
            ("Juan", "Nuevo Testamento", "Juan", "70-100 d.C.", "Asia Menor", "Éfeso", "Jesús, Vida Eterna"),
            ("Hechos", "Nuevo Testamento", "Lucas", "60-80 d.C.", "Grecia", "Aquea", "Iglesia, Espíritu"),
            ("Romanos", "Nuevo Testamento", "Pablo", "57-58 d.C.", "Corinto", "Corinto", "Gracia, Fe"),
            ("1 Corintios", "Nuevo Testamento", "Pablo", "55 d.C.", "Éfeso", "Éfeso", "Iglesia, Amor"),
            ("Gálatas", "Nuevo Testamento", "Pablo", "48-55 d.C.", "Galacia", "Antioquía", "Libertad, Fe"),
            ("Efesios", "Nuevo Testamento", "Pablo", "60-62 d.C.", "Roma", "Roma", "Iglesia, Unión"),
            ("Filipenses", "Nuevo Testamento", "Pablo", "60-62 d.C.", "Roma", "Roma", "Gozo, Fortaleza"),
            ("Hebreos", "Nuevo Testamento", "Anónimo", "60-90 d.C.", "Israel", "Jerusalén", "Cristo, Fe"),
            ("Santiago", "Nuevo Testamento", "Santiago", "45-50 d.C.", "Israel", "Jerusalén", "Fe y Obras"),
            ("1 Pedro", "Nuevo Testamento", "Pedro", "60-65 d.C.", "Roma", "Roma", "Esperanza, Sufrimiento"),
            ("1 Juan", "Nuevo Testamento", "Juan", "70-100 d.C.", "Asia Menor", "Éfeso", "Amor, Verdad"),
            ("Apocalipsis", "Nuevo Testamento", "Juan", "90-95 d.C.", "Asia Menor", "Patmos", "Victoria, Futuro")
        ]
        for l in libros:
            c.execute("INSERT INTO libros VALUES (NULL,?,?,?,?,?,?,?)", l)
    
    # Versículos
    c.execute("""CREATE TABLE IF NOT EXISTS versiculos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        libro TEXT,
        capitulo INTEGER,
        versiculo INTEGER,
        texto TEXT
    )""")
    
    c.execute("SELECT COUNT(*) FROM versiculos")
    if c.fetchone()[0] == 0:
        versiculos = [
            ("Génesis", 1, 1, "En el principio creó Dios los cielos y la tierra."),
            ("Génesis", 1, 27, "Y creó Dios al hombre a su imagen, a imagen de Dios lo creó; varón y hembra los creó."),
            ("Josué", 1, 9, "Mira que te mando que te esfuerces y seas valiente; no temas ni desmayes, porque Jehová tu Dios estará contigo en dondequiera que vayas."),
            ("Salmo", 23, 1, "Jehová es mi pastor; nada me faltará."),
            ("Salmo", 119, 105, "Lámpara es a mis pies tu palabra, y lumbrera a mi camino."),
            ("Proverbios", 3, 5, "Fíate de Jehová de todo tu corazón, y no te apoyes en tu propia prudencia."),
            ("Isaías", 41, 10, "No temas, porque yo estoy contigo; no desmayes, porque yo soy tu Dios que te esfuerzo."),
            ("Jeremías", 29, 11, "Porque yo sé los planes que tengo para vosotros, dice Jehová, planes de paz y no de mal, para daros un futuro y una esperanza."),
            ("Mateo", 11, 28, "Venid a mí todos los que estáis cansados y cargados, y yo os haré descansar."),
            ("Juan", 3, 16, "Porque de tal manera amó Dios al mundo, que ha dado a su Hijo unigénito, para que todo aquel que en él cree, no se pierda, mas tenga vida eterna."),
            ("Juan", 14, 6, "Jesús le dijo: Yo soy el camino, y la verdad, y la vida; nadie viene al Padre, sino por mí."),
            ("Hechos", 16, 31, "Cree en el Señor Jesucristo, y serás salvo, tú y tu casa."),
            ("Romanos", 8, 28, "Y sabemos que a los que aman a Dios, todas las cosas les ayudan a bien."),
            ("1 Corintios", 13, 4, "El amor es sufrido, es benigno; el amor no tiene envidia, el amor no es jactancioso, no se envanece."),
            ("1 Corintios", 13, 13, "Y ahora permanecen la fe, la esperanza y el amor, estos tres; pero el mayor de ellos es el amor."),
            ("Gálatas", 5, 22, "Mas el fruto del Espíritu es: amor, gozo, paz, paciencia, benignidad, bondad, fe."),
            ("Efesios", 2, 8, "Porque por gracia sois salvos por medio de la fe; y esto no de vosotros, pues es don de Dios."),
            ("Filipenses", 4, 6, "Por nada estéis afanosos, sino sean conocidas vuestras peticiones delante de Dios en toda oración y ruego, con acción de gracias."),
            ("Filipenses", 4, 13, "Todo lo puedo en Cristo que me fortalece."),
            ("Hebreos", 11, 1, "Es, pues, la fe la certeza de lo que se espera, la convicción de lo que no se ve."),
            ("Santiago", 1, 5, "Y si alguno de vosotros tiene falta de sabiduría, pídala a Dios, el cual da a todos abundantemente y sin reproche, y le será dada."),
            ("1 Pedro", 5, 7, "Echando toda vuestra ansiedad sobre él, porque él tiene cuidado de vosotros."),
            ("1 Juan", 4, 19, "Nosotros amamos a él, porque él nos amó primero."),
            ("Apocalipsis", 21, 4, "Y enjugará Dios toda lágrima de los ojos de ellos; y ya no habrá muerte, ni habrá más llanto, ni clamor, ni dolor.")
        ]
        for v in versiculos:
            c.execute("INSERT INTO versiculos VALUES (NULL,?,?,?,?)", v)
    
    # Lugares
    c.execute("""CREATE TABLE IF NOT EXISTS lugares (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        tipo TEXT,
        latitud REAL,
        longitud REAL,
        descripcion TEXT
    )""")
    
    c.execute("SELECT COUNT(*) FROM lugares")
    if c.fetchone()[0] == 0:
        lugares = [
            ("Monte Sinaí", "Escritura", 28.5267, 33.9767, "Aquí Dios dio la Ley a Moisés. Lugar donde se escribieron los primeros libros de la Biblia."),
            ("Jerusalén", "Ciudad santa", 31.7683, 35.2137, "Ciudad santa, centro espiritual. Muchos libros fueron escritos aquí o desde aquí."),
            ("Belén", "Nacimiento", 31.7047, 35.1979, "Ciudad donde nació Jesús y de donde era el rey David."),
            ("Babilonia", "Exilio", 32.5463, 44.4286, "Aquí estuvieron los israelitas en el exilio. Libros como Daniel y Ezequiel se escribieron aquí."),
            ("Roma", "Escritura", 41.9028, 12.4964, "Desde aquí Pablo escribió muchas cartas mientras estaba prisionero."),
            ("Antioquía", "Escritura", 36.2012, 36.1559, "Donde se escribieron Mateo y Gálatas. Aquí llamaron cristianos por primera vez a los creyentes."),
            ("Éfeso", "Escritura", 37.9450, 27.3654, "Ciudad importante en Asia Menor. Aquí escribió Juan sus cartas y Pablo vivió un tiempo."),
            ("Patmos", "Isla", 37.3044, 26.5622, "Isla donde Juan estuvo exiliado y recibió la visión del Apocalipsis."),
            ("Corinto", "Escritura", 37.9379, 22.9322, "Ciudad comercial donde Pablo escribió Romanos y 1 Corintios."),
            ("Moab", "Escritura", 31.4647, 35.6584, "Lugar donde Moisés escribió Deuteronomio antes de morir.")
        ]
        for l in lugares:
            c.execute("INSERT INTO lugares VALUES (NULL,?,?,?,?,?)", l)
    
    conn.commit()
    return conn

conn = init_data()

# ==========================================
# INTERFAZ
# ==========================================
st.title("✝️ 📖 Biblia: Aprende, Memoriza y Navega")
st.subheader("¡Explora la Palabra de Dios de forma divertida! 🎯")

menu = st.sidebar.radio("📋 Menú Principal", [
    "🏠 Inicio",
    "📖 Libros y Versículos",
    "🧠 Memorizar Versículos",
    "🔍 Buscar y Concordancia",
    "🗺️ Mapa Bíblico",
    "📚 Información de Libros"
])

# ---------- INICIO ----------
if menu == "🏠 Inicio":
    st.header("¡Bienvenido! 🎉")
    st.info("""
    Esta aplicación te ayuda a:
    - ✅ Navegar por los libros de la Biblia
    - ✅ Memorizar versículos con tarjetas interactivas
    - ✅ Encontrar versículos relacionados por palabras
    - ✅ Conocer dónde se escribió cada libro
    - ✅ Ubicar lugares importantes de la Biblia
    """)
    
    import random
    c = conn.cursor()
    c.execute("SELECT libro, capitulo, versiculo, texto FROM versiculos ORDER BY RANDOM() LIMIT 1")
    v = c.fetchone()
    if v:
        st.subheader("✨ Versículo del día")
        st.success(f"**{v[0]} {v[1]}:{v[2]}**")
        st.write(v[3])

# ---------- LIBROS Y VERSÍCULOS ----------
elif menu == "📖 Libros y Versículos":
    st.header("📖 Libros de la Biblia")
    df_libros = pd.read_sql("SELECT nombre FROM libros ORDER BY id", conn)
    lista_libros = df_libros["nombre"].tolist()
    seleccion = st.selectbox("📚 Selecciona un libro:", lista_libros)
    
    if seleccion:
        st.subheader(f"📝 Versículos de {seleccion}")
        df_v = pd.read_sql("SELECT capitulo, versiculo, texto FROM versiculos WHERE libro = ?", conn, params=(seleccion,))
        if not df_v.empty:
            for _, row in df_v.iterrows():
                st.write(f"**{row['capitulo']}:{row['versiculo']}** — {row['texto']}")
                st.divider()
        else:
            st.info("Más versículos próximamente 😊")

# ---------- MEMORIZAR ----------
elif menu == "🧠 Memorizar Versículos":
    st.header("🧠 ¡Aprende memorizando!")
    
    c = conn.cursor()
    c.execute("SELECT libro, capitulo, versiculo, texto FROM versiculos ORDER BY RANDOM() LIMIT 1")
    v = c.fetchone()
    
    if 'versiculo_actual' not in st.session_state:
        st.session_state.versiculo_actual = v
    
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("🎲 Nuevo Versículo"):
            c.execute("SELECT libro, capitulo, versiculo, texto FROM versiculos ORDER BY RANDOM() LIMIT 1")
            v = c.fetchone()
            st.session_state.versiculo_actual = v
    
    if 'versiculo_actual' in st.session_state:
        v = st.session_state.versiculo_actual
        st.subheader(f"📖 {v[0]} {v[1]}:{v[2]}")
        
        mostrar = st.checkbox("👀 Mostrar el versículo")
        if mostrar:
            st.info(v[3])
        else:
            st.write("❓ Intenta recordarlo 👆")

# ---------- BUSCAR ----------
elif menu == "🔍 Buscar y Concordancia":
    st.header("🔍 Buscar Versículos")
    st.write("Escribe una palabra para encontrar todos los versículos relacionados.")
    
    palabra = st.text_input("✏️ Escribe una palabra:")
    if palabra:
        c = conn.cursor()
        c.execute("SELECT libro, capitulo, versiculo, texto FROM versiculos WHERE texto LIKE ?", (f"%{palabra}%",))
        resultados = c.fetchall()
        
        if resultados:
            st.success(f"✅ Encontré {len(resultados)} versículos:")
            for r in resultados:
                st.write(f"📌 **{r[0]} {r[1]}:{r[2]}** — {r[3]}")
        else:
            st.warning("No encontré versículos con esa palabra. Intenta con otra 😊")

# ---------- MAPA ----------
elif menu == "🗺️ Mapa Bíblico":
    st.header("🗺️ Lugares de la Biblia")
    df_lugares = pd.read_sql("SELECT * FROM lugares", conn)
    
    for _, row in df_lugares.iterrows():
        with st.expander(f"📍 {row['nombre']} — {row['tipo']}"):
            st.write(f"🌍 **Coordenadas:** {row['latitud']}, {row['longitud']}")
            st.write(f"📝 {row['descripcion']}")
        st.divider()

# ---------- INFO DE LIBROS ----------
elif menu == "📚 Información de Libros":
    st.header("📚 Conoce cada libro")
    df_libros = pd.read_sql("SELECT * FROM libros", conn)
    
    for _, row in df_libros.iterrows():
        with st.expander(f"📖 {row['nombre']} — {row['testamento']}"):
            st.write(f"✍️ **Escrito por:** {row['autor']}")
            st.write(f"📅 **Fecha aproximada:** {row['fecha']}")
            st.write(f"📍 **Lugar:** {row['lugar_exacto']} ({row['lugar_escritura']})")
            st.write(f"💡 **Temas principales:** {row['temas']}")
        st.divider()

st.divider()
st.caption("✝️ Que la Palabra de Dios te acompañe siempre 🙏")
