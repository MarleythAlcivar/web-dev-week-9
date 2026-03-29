"""
Generador de reportes PDF para el sistema CRUD
"""

from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
import os

class PDFGenerator:
    """Clase para generar reportes PDF"""
    
    def __init__(self, filename=None):
        self.filename = filename or f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configurar estilos personalizados"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1,  # Center alignment
            textColor=colors.darkblue
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            textColor=colors.darkblue
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6
        ))
    
    def generate_product_report(self, productos, title="Reporte de Productos"):
        """Generar reporte de productos en PDF"""
        try:
            # Crear directorio reports si no existe
            reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
            if not os.path.exists(reports_dir):
                os.makedirs(reports_dir)
            
            # Ruta completa del archivo
            filepath = os.path.join(reports_dir, self.filename)
            
            # Crear documento
            doc = SimpleDocTemplate(
                filepath,
                pagesize=landscape(letter),
                rightMargin=30,
                leftMargin=30,
                topMargin=30,
                bottomMargin=30
            )
            
            # Contenido del reporte
            elements = []
            
            # Título
            elements.append(Paragraph(title, self.styles['CustomTitle']))
            
            # Fecha de generación
            fecha_generacion = f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
            elements.append(Paragraph(fecha_generacion, self.styles['CustomNormal']))
            elements.append(Spacer(1, 20))
            
            # Estadísticas
            if productos:
                total_productos = len(productos)
                valor_total = sum(p['precio'] * p['stock'] for p in productos)
                stock_total = sum(p['stock'] for p in productos)
                
                stats_data = [
                    ['Estadísticas Generales', ''],
                    ['Total de productos:', str(total_productos)],
                    ['Valor total del inventario:', f"${valor_total:,.2f}"],
                    ['Stock total:', str(stock_total)],
                    ['Promedio de stock:', f"{stock_total / total_productos:.1f}" if total_productos > 0 else "0"]
                ]
                
                stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
                stats_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                elements.append(stats_table)
                elements.append(Spacer(1, 30))
            
            # Tabla de productos
            if productos:
                elements.append(Paragraph("Detalle de Productos", self.styles['CustomHeading']))
                
                # Preparar datos de la tabla
                headers = ['ID', 'Nombre', 'Descripción', 'Categoría', 'Precio', 'Stock', 'Valor Total']
                table_data = [headers]
                
                for producto in productos:
                    # Truncar descripción si es muy larga
                    descripcion = producto['descripcion'][:50] + "..." if len(producto['descripcion']) > 50 else producto['descripcion']
                    valor_total = producto['precio'] * producto['stock']
                    
                    row = [
                        str(producto['id_producto']),
                        producto['nombre'][:20] + "..." if len(producto['nombre']) > 20 else producto['nombre'],
                        descripcion,
                        producto['categoria'] or 'Sin categoría',
                        f"${producto['precio']:,.2f}",
                        str(producto['stock']),
                        f"${valor_total:,.2f}"
                    ]
                    table_data.append(row)
                
                # Crear tabla
                table = Table(table_data, colWidths=[0.5*inch, 2*inch, 2.5*inch, 1.2*inch, 0.8*inch, 0.6*inch, 0.8*inch])
                
                # Estilo de la tabla
                table.setStyle(TableStyle([
                    # Encabezado
                    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    
                    # Cuerpo de la tabla
                    ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    
                    # Alineación de columnas específicas
                    ('ALIGN', (4, 1), (6, -1), 'RIGHT'),  # Precio, Stock, Valor Total
                    
                    # Colores alternados
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
                ]))
                
                elements.append(table)
            else:
                elements.append(Paragraph("No hay productos para mostrar en este reporte.", self.styles['CustomNormal']))
            
            # Generar PDF
            doc.build(elements)
            
            return {
                'success': True,
                'filepath': filepath,
                'filename': self.filename,
                'message': 'Reporte PDF generado exitosamente'
            }
            
        except Exception as e:
            return {
                'success': False,
                'filepath': None,
                'filename': None,
                'message': f'Error al generar PDF: {str(e)}'
            }
    
    def generate_low_stock_report(self, productos, title="Reporte de Productos con Bajo Stock"):
        """Generar reporte de productos con bajo stock"""
        try:
            # Crear directorio reports si no existe
            reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
            if not os.path.exists(reports_dir):
                os.makedirs(reports_dir)
            
            # Ruta completa del archivo
            filepath = os.path.join(reports_dir, self.filename)
            
            # Crear documento
            doc = SimpleDocTemplate(
                filepath,
                pagesize=letter,
                rightMargin=30,
                leftMargin=30,
                topMargin=30,
                bottomMargin=30
            )
            
            # Contenido del reporte
            elements = []
            
            # Título
            elements.append(Paragraph(title, self.styles['CustomTitle']))
            
            # Fecha de generación
            fecha_generacion = f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
            elements.append(Paragraph(fecha_generacion, self.styles['CustomNormal']))
            elements.append(Spacer(1, 20))
            
            # Alerta
            if productos:
                alerta = Paragraph("⚠️ ALERTA: Productos con stock bajo o agotado", self.styles['CustomHeading'])
                elements.append(alerta)
                elements.append(Spacer(1, 20))
            
            # Tabla de productos con bajo stock
            if productos:
                headers = ['ID', 'Nombre', 'Categoría', 'Stock Actual', 'Precio', 'Estado']
                table_data = [headers]
                
                for producto in productos:
                    # Determinar estado según el stock
                    stock = producto['stock']
                    if stock == 0:
                        estado = "AGOTADO"
                        estado_color = colors.red
                    elif stock <= 5:
                        estado = "CRÍTICO"
                        estado_color = colors.orange
                    else:
                        estado = "BAJO"
                        estado_color = colors.yellow
                    
                    row = [
                        str(producto['id_producto']),
                        producto['nombre'],
                        producto['categoria'] or 'Sin categoría',
                        str(stock),
                        f"${producto['precio']:,.2f}",
                        estado
                    ]
                    table_data.append(row)
                
                # Crear tabla
                table = Table(table_data, colWidths=[0.5*inch, 2.5*inch, 1.5*inch, 1*inch, 1*inch, 1*inch])
                
                # Estilo de la tabla
                table.setStyle(TableStyle([
                    # Encabezado
                    ('BACKGROUND', (0, 0), (-1, 0), colors.darkred),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    
                    # Cuerpo de la tabla
                    ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    
                    # Alineación de columnas específicas
                    ('ALIGN', (3, 1), (4, -1), 'RIGHT'),  # Stock, Precio
                    ('ALIGN', (5, 1), (5, -1), 'CENTER'),  # Estado
                    
                    # Colores según estado
                    ('TEXTCOLOR', (5, 1), (5, -1), colors.red)  # Columna de estado en rojo
                ]))
                
                elements.append(table)
                
                # Recomendaciones
                elements.append(Spacer(1, 30))
                elements.append(Paragraph("Recomendaciones:", self.styles['CustomHeading']))
                
                recomendaciones = [
                    "1. Reabastecer productos con stock crítico (≤ 5 unidades) inmediatamente",
                    "2. Considerar realizar pedidos de productos agotados (0 unidades)",
                    "3. Monitorear productos con bajo stock (≤ 10 unidades) semanalmente",
                    "4. Establecer puntos de reorden automáticos para evitar desabastecimiento"
                ]
                
                for rec in recomendaciones:
                    elements.append(Paragraph(rec, self.styles['CustomNormal']))
                    elements.append(Spacer(1, 6))
            else:
                elements.append(Paragraph("✅ Todos los productos tienen niveles de stock adecuados.", self.styles['CustomNormal']))
            
            # Generar PDF
            doc.build(elements)
            
            return {
                'success': True,
                'filepath': filepath,
                'filename': self.filename,
                'message': 'Reporte de bajo stock generado exitosamente'
            }
            
        except Exception as e:
            return {
                'success': False,
                'filepath': None,
                'filename': None,
                'message': f'Error al generar PDF de bajo stock: {str(e)}'
            }
