# imports
import pygame
import neat 
import pickle

from game_objects import *

# Initilizations
gen = 0
win_width = 500
win_height = 800

pygame.font.init()
font = pygame.font.SysFont("comicsans", 30)

background = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "background.png")))

# Training
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    poppulation = neat.Population(config)
    poppulation.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    poppulation.add_reporter(stats)

    winner = poppulation.run(inference_mode, 500) # run for 500 generations, then quit
    with open('best_bird.pickle', 'wb') as f: # save the "fittest" bird
        pickle.dump(winner, f)

# Showcase Mode
def showcase_best_bird(net):
    bird = Bird(230, 350)
    base = Base(730)
    window = pygame.display.set_mode((win_width, win_height))
    pipes = [Pipe(700)]
    score = 0
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        
        # decision making using the loaded model
        pipe_index = 0
        if len(pipes) > 1 and bird.x > pipes[0].x + pipes[0].pipe_top.get_width():
            pipe_index = 1

        output = net.activate((bird.y, abs(bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].bottom)))
        if output[0] > 0.5:
            bird.jump()

        bird.move()
        base.move()
        
        add_pipe = False
        rem = []
        for pipe in pipes:
            if pipe.collide(bird):
                run = False 
                break

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            
            if pipe.x + pipe.pipe_top.get_width() < 0: 
                rem.append(pipe)
                
            pipe.move()
        
        if add_pipe:
            score += 1
            pipes.append(Pipe(550))
            
        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
            run = False
        
        draw_window(window, [bird], pipes, base, score, 0, mode='showcase')

def load_bird_model(): 
    with open("best_bird.pkl", "rb") as f:
        return pickle.load(f)
    
# Actual Run for Training and Showcasing
def inference_mode(genomes, config):
    global gen
    gen +=1 # keep track of the generation

    nets = []
    ge = []
    birds = []
    
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(730)
    
    window = pygame.display.set_mode((win_width, win_height))
    clock = pygame.time.Clock()
    pipes = [Pipe(700)]
    
    
    score = 0
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        pipe_index = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].pipe_top.get_width():
                pipe_index = 1
        else:
            run = False
            break # failsave

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            # save a bird which fitness score exceeds a given value
            # check if fitness exceeds 150
            if ge[x].fitness > 150:
                with open("best_bird.pkl", "wb") as f:
                    pickle.dump(nets[x], f)
                print("Best bird saved with fitness:", ge[x].fitness)

            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].bottom)))

            if output[0] > 0.5:
                bird.jump()
                
        base.move()
        remove = []
        add_pipe = False
        for pipe in pipes:
            for x, bird in enumerate(birds):

                if pipe.collide(bird):
                    ge[x].fitness -= 1 # dont faviour birds that have collided with pipes
                    birds.pop(x) # get rid of bird object 
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
            
            if pipe.x + pipe.pipe_top.get_width() < 0: 
                remove.append(pipe)  

            pipe.move()
        
        if add_pipe:
            score += 1 
            for g in ge:
                g.fitness += 3 # reward for passing through the pipes
            pipes.append(Pipe(600)) # adjustments here change the spawn distance of pipes 
            
        for r in remove:
            pipes.remove(r)
        
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        if ge:  
            max_fitness_value = max([g.fitness for g in ge])
            max_fitness_value = round(max_fitness_value)
        else:
            max_fitness_value = 0

        draw_window(window, birds, pipes, base, score, gen, max_fitness=max_fitness_value, mode='auto')

# Manual Mode
def manual_mode(initial_start=True): 
    bird = Bird(230, 350)
    base = Base(730)
    
    window = pygame.display.set_mode((win_width, win_height))
    clock = pygame.time.Clock()
    pipes = [Pipe(700)]
    
    score = 0
    run = True
    game_over = False
    game_started = False if initial_start else True  # only show start button for the initial start
    restart_button = Button(win_width // 2 - 70, win_height // 2, 140, 40, 'Restart')
    start_button = Button(win_width // 2 - 70, win_height // 2, 140, 40, 'Start')
    
    if initial_start:
        while not game_started:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    game_started = True 
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if start_button.click(pos):
                        game_started = True
            draw_window(window, [bird], pipes, base, score, 0, mode='manual')
            start_button.draw(window)
            pygame.display.update()

    while run and game_started:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.jump()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if game_over and restart_button.click(pos):
                    manual_mode(initial_start=False)  
                    return
        bird.move()
        base.move()
        
        remove = []
        add_pipe = False
        for pipe in pipes:
            if pipe.collide(bird):
                game_over = True
                bird.velocity = 0 
            
            if not game_over:
                if pipe.x + pipe.pipe_top.get_width() < 0: 
                    remove.append(pipe)
                
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
                pipe.move()
        
        if add_pipe:
            score += 1 
            pipes.append(Pipe(600))
            
        for r in remove:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
            game_over = True
        
        draw_window(window, [bird], pipes, base, score, 0, mode='manual')
        
        if game_over:
            bird.velocity = 0
            base.velocity = 0 
            restart_button.draw(window)
            
        pygame.display.update()

# Displaying Relevant Text
def draw_window(window, birds, pipes, base, score, gen, max_fitness=None, mode='auto'):
    window.blit(background, (0, 0))
    
    for pipe in pipes:
        pipe.draw(window)
    for bird in birds:
        bird.draw(window)

    text = font.render("Score: " + str(score), 1, (255, 255, 255))
    window.blit(text, (win_width - 10 - text.get_width(), 10))

    if mode == 'showcase':
        text = font.render("Showcase Mode", 1, (255, 255, 255))
    elif mode == 'manual':
        text = font.render("Manual Mode", 1, (255, 255, 255))
    else:  
        text = font.render("Generation: " + str(gen), 1, (255, 255, 255))
    window.blit(text, (10, 10))

    if max_fitness is not None:
        fitness_text = font.render("Max Fitness: " + str(max_fitness), 1, (255, 255, 255))
        window.blit(fitness_text, (10, 50))

    base.draw(window)
    pygame.display.update()