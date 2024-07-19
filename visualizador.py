import pygame
import sys
import time

class Visualizador:
    def __init__(self, procesador):
        self.procesador = procesador
        self.width = 1200
        self.height = 800
        self.bg_color = (28, 28, 27)
        self.font_color = (168, 186, 188)
        self.font_size = 30
        self.line_height = 25
        self.cell_size = 20

        # Colores de fondo para cada sección
        self.color_instrucciones = (28, 28, 27)  # Gris Claro
        self.color_registros = (18, 45, 47)  # turqueza oscuro
        self.color_pila = (28, 82, 87)  # turqueza semi oscuro
        self.color_video_memoria = (37, 108, 114)  # turqueza claro
        self.color_resaltado = (28, 82, 87)  #

        # Inicializar desplazamiento
        self.scroll_offset = 0

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Visualizador')
        self.font = pygame.font.Font(None, self.font_size)
        self.clock = pygame.time.Clock()

    def mostrar_pantalla(self, ejecutable):
        self.screen.fill(self.bg_color)

        # Coordenadas y tamaños para las secciones
        left_width = self.width // 2
        right_width = self.width // 2
        section_height = self.height // 3

        instrucciones_rect = pygame.Rect(0, 0, left_width, self.height)
        self.draw_rounded_rect(self.screen, self.color_instrucciones, instrucciones_rect, 20)

        # Cuadro redondeado interior (otro color)
        interior_instrucciones_rect = pygame.Rect(10, 10, left_width - 50, self.height - 50)  # Ajusta los márgenes
        self.draw_rounded_rect(self.screen, (28, 28, 27), interior_instrucciones_rect,
                               20)  # Cambia el color (por ejemplo, Gris Oscuro)

        # Calcular desplazamiento para que la instrucción actual sea visible
        ip = self.procesador.registros['ip']
        visible_lines = (interior_instrucciones_rect.height - 20) // self.line_height
        if ip < self.scroll_offset:
            self.scroll_offset = ip
        elif ip >= self.scroll_offset + visible_lines:
            self.scroll_offset = ip - visible_lines + 1

        # Mostrar instrucciones con desplazamiento
        instrucciones_text = "Instrucciones:\n" + "\n".join(
            [f" -> {linea}" if i == ip else f"    {linea}"
             for i, linea in enumerate(ejecutable.codigo)]
        )
        self.draw_text(instrucciones_text, 20, 20, ip - self.scroll_offset)

        # Mostrar registros
        self.draw_registros(left_width, right_width, section_height)

        # Mostrar pila
        pila_rect = pygame.Rect(left_width, section_height, right_width, section_height)
        self.draw_rounded_rect(self.screen, self.color_pila, pila_rect, 20)
        self.draw_stack(ejecutable.pila, left_width + 10, section_height + 10, right_width - 20, section_height - 20)

        # Mostrar memoria de video
        video_memory_rect = pygame.Rect(left_width, 2 * section_height, right_width, section_height)
        self.draw_rounded_rect(self.screen, self.color_video_memoria, video_memory_rect, 20)
        self.draw_video_memory(self.procesador.proceso_actual.pantalla, left_width + 10, 2 * section_height + 10)

        pygame.display.flip()

    def draw_text(self, text, x, y, highlight_index=None):
        lines = text.split('\n')
        lines = lines[self.scroll_offset:]  # Aplicar desplazamiento
        for i, line in enumerate(lines):
            line_surface = self.font.render(line, True, self.font_color)
            self.screen.blit(line_surface, (x, y))
            y += self.line_height

    def draw_registros(self, left_width, right_width, section_height):
        # Dibujar rectángulo de fondo para registros
        registros_rect = pygame.Rect(left_width, 0, right_width, section_height)
        self.draw_rounded_rect(self.screen, self.color_registros, registros_rect, 20)

        # Dibujar título "Registros"
        title_surface = self.font.render("Registros", True, self.font_color)
        self.screen.blit(title_surface, (left_width + 10, 10))

        # Dibujar cada registro y su valor
        y = 40  # Posición inicial para los registros
        for registro, valor in self.procesador.registros.items():
            registro_text = f"{registro}: {valor}"
            registro_surface = self.font.render(registro_text, True, self.font_color)
            self.screen.blit(registro_surface, (left_width + 20, y))
            y += self.line_height

    def draw_stack(self, stack, x, y, width, height):
        # Dibujar el título "Pila"
        title_surface = self.font.render("Pila", True, self.font_color)
        self.screen.blit(title_surface, (x, y))
        y += self.line_height + 5  # Dejar un pequeño espacio después del título

        # Determinar el tamaño de cada elemento de la pila
        element_height = (height - self.line_height - 5) // len(stack) if stack else 0

        # Dibujar cada elemento de la pila
        for i, elemento in enumerate(reversed(stack)):
            pygame.draw.rect(
                self.screen,
                (200, 200, 200),  # Color del borde del elemento de la pila
                pygame.Rect(x, y + i * element_height, width, element_height),
                1  # Grosor del borde
            )
            element_surface = self.font.render(str(elemento), True, self.font_color)
            self.screen.blit(element_surface, (x + 5, y + i * element_height + 5))

    def draw_video_memory(self, video_memory, x, y):
        # Dibujar el título "Memoria de Video"
        title_surface = self.font.render("Memoria de Video", True, self.font_color)
        self.screen.blit(title_surface, (x, y))
        y += self.line_height + 5  # Dejar un pequeño espacio después del título

        # Dibujar la matriz de memoria de video
        for row_index, row in enumerate(video_memory):
            for col_index, cell_value in enumerate(row):
                # Determinar el color de fondo de la celda
                cell_color = (255, 0, 0) if cell_value != 0 else (0, 0, 0)

                # Dibujar celda
                cell_rect = pygame.Rect(x + col_index * self.cell_size, y + row_index * self.cell_size, self.cell_size,
                                        self.cell_size)
                pygame.draw.rect(self.screen, cell_color, cell_rect)
                pygame.draw.rect(self.screen, (0, 0, 0), cell_rect, 1)  # Borde de la celda

                # Renderizar el valor numérico dentro de la celda como entero
                cell_value_surface = self.font.render(str(int(cell_value)), True, self.font_color)
                cell_value_rect = cell_value_surface.get_rect(center=cell_rect.center)
                self.screen.blit(cell_value_surface, cell_value_rect)

        pygame.display.update(
            pygame.Rect(x, y, len(video_memory[0]) * self.cell_size, len(video_memory) * self.cell_size))

    def draw_rounded_rect(self, surface, color, rect, radius):
        """Dibuja un rectángulo con bordes redondeados en la superficie dada."""
        pygame.draw.rect(surface, color, rect, border_radius=radius)

    def run(self, ejecutable):
        self.ejecutable = ejecutable
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.mostrar_pantalla(ejecutable)
            self.clock.tick(120)

        self.wait_for_exit()

    def wait_for_exit(self):
        """Espera a que el usuario presione Enter para salir."""
        print("Presiona Enter para salir...")
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting = False
        pygame.quit()