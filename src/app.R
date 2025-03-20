options(shiny.port = 8050, shiny.autoreload = TRUE)

library(shiny)
library(bslib)
library(dplyr)
library(ggplot2)
library(thematic)
library(plotly)
library(ggtext)

#import and organize data
ee <- read.csv('../data/raw/EE.csv')
ee$date <- as.Date(ee$date, format = "%m/%d/%Y")

ee_pool <- read.csv('../data/raw/EE_pool.csv')
colnames(ee_pool) <- gsub("^X", "", colnames(ee_pool))
ee_pool$date <- as.Date(ee_pool$date, format = "%m/%d/%Y")


# Layout
ui <- page_fluid( 
    theme = bs_theme(version = 5, 
                     base_font = font_google("Roboto"), 
                     bootswatch = "minty"),
    h1("Express Entry", style = "font-family: 'Roboto', sans-serif; font-size: 26px;"),
    p("Data collected from Jan/01/2023 to Mar/17/2025.", style = "font-family: 'Roboto', sans-serif;font-size: 10px;"),
    
    br(),
    
    div(
      style = "display: flex;",
      fluidRow(
        column(
          width = 2,
          
          textInput("input_CRS", "Enter your CRS:"),
          
          selectInput(
            'x_col',
            'Select A Category',
            choices = c("invitations_issued", "CRS_score"),
            selected = "CRS_score"),
          
          selectizeInput(
            "draw_type_multi",
            "Draw Type(s)",
            choices = unique(ee$type),
            multi=TRUE,
            selected = "CEC",
            options = list(placeholder = 'Please select ...',
                           plugins = list("remove_button"))),
          ),
        
        column(
          width = 10,
          plotlyOutput("plot", width = 1200, height = 200),
          br(),
          plotOutput("facet_plot", width = 800, height = 400)
        )
      )
    ),

)


# Server side callbacks/reactivity
server <- function(input, output, session) {
  #line plot showing draw score trends
  output$plot <- renderPlotly({
    
    if (length(input$draw_type_multi) == 0){
      ee_filtered <- ee
    }
    else {
      ee_filtered <- ee |> 
        filter(type %in% input$draw_type_multi)
    }
      
    plot <- ggplot(ee_filtered, 
             aes(x = date, y = !!sym(input$x_col), group = type, color = type,
                 text = paste("Date: ", date, "<br>", 
                              "Value: ", !!sym(input$x_col))
                 )) +
        geom_line() +
        geom_point() +
        labs(x = "Date",
             y = input$x_col,
             color = "Draw Type") +
        scale_x_date(limits = range(ee_filtered$date),
                     date_labels = "%b %Y") +
      geom_hline(yintercept = as.numeric(input$input_CRS), linetype="longdash", col='darkred') +
      annotate("text", x = max(ee_filtered$date), y = as.numeric(input$input_CRS) + 4.7,  
               label = "🍁", size = 8) + 
        theme_minimal()
    
    ggplotly(plot, tooltip = "text")
  })
  
  #stack plot showing score range changes
  output$facet_plot <- renderPlot({
    
    ee_pool_longer <- ee_pool |> 
      select(date, change_601, change_501, change_451, change_401, change_351, change_301, change_0) |> 
      pivot_longer(!date, names_to = "range", values_to = "size") |> 
      mutate(range = factor(range, levels = c("change_601", "change_501", "change_451", "change_401", "change_351", "change_301", "change_0")))
    
    
    ggplot(ee_pool_longer,
           aes(x = date,
               y = size,
               fill = range)) +
      geom_bar(stat = "identity", position = "stack", width = 8, alpha = 0.5) +
      labs(x = NULL, y = NULL) +
      scale_x_date(date_labels = "%b %Y") +
      theme_minimal()
  })
  

}

# Run the app/dashboard
shinyApp(ui, server)








