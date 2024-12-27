
use bevy::{audio::PlaybackMode, utils::label};
use rusty_engine::prelude::*;

#[derive(Resource)]
struct GameState{
    high_score: i32,
    score: i32,
    fire_index: i32,
    spawn_timer: Timer,
} 

impl Default for GameState {
    fn default() -> Self {
        Self {
            high_score: 0,
            score: 0,
            fire_index: 0,
            spawn_timer: Timer::from_seconds(1.0, TimerMode::Once),
        }
    }
}
fn main() {
    let mut game = Game::new();
    
    // setup game 
    let player = game.add_sprite("player", SpritePreset::RacingCarBlue);
    player.translation = Vec2::new(0.0, 0.0);
    player.rotation = UP;
    player.scale = 1.0;
    player.layer = 1.0;
    player.collision = true;    

    let score = game.add_text("score", "Score: 0");
    score.translation = Vec2::new(520.0, 320.0);

    let high_score = game.add_text("high_score", "High Score: 0");
    high_score.translation = Vec2::new(-520.0, 320.0);

    game.add_logic(game_logic);
    game.run(GameState::default());
}

fn game_logic(engine: &mut Engine, game_state: &mut GameState) {
    // handle collision events
    //engine.show_colliders = true;
    for event in engine.collision_events.drain(..){
        //println!("Collision event: {:#?}", event);
        if event.state == CollisionState::Begin && event.pair.one_starts_with("player"){
            // remove the sprite that the player collided with
            for lable in [event.pair.0, event.pair.1] {
                if lable != "player" {
                    engine.sprites.remove(&lable);
                }
            }
            game_state.score += 1;
            let score = engine.texts.get_mut("score").unwrap();
            score.value = format!("Score: {}", game_state.score);
            if game_state.score > game_state.high_score {
                game_state.high_score = game_state.score;
                let high_score = engine.texts.get_mut("high_score").unwrap();
                high_score.value = format!("High Score: {}", game_state.high_score);
            }
        }
    }
    
    // handle movement
    let player = engine.sprites.get_mut("player").unwrap();
    //player.translation.x += 100.0 * engine.delta_f32;
    const MOVMENT_SPEED: f32 = 200.0;
    if engine.keyboard_state.pressed_any(&[KeyCode::Up,KeyCode::W]){ 
        player.translation.y += MOVMENT_SPEED * engine.delta_f32;
    }
    if engine.keyboard_state.pressed_any(&[KeyCode::Down,KeyCode::S]){ 
        player.translation.y -= MOVMENT_SPEED * engine.delta_f32;
    }
    if engine.keyboard_state.pressed_any(&[KeyCode::Left,KeyCode::A]){ 
        player.translation.x -= MOVMENT_SPEED * engine.delta_f32;
    }
    if engine.keyboard_state.pressed_any(&[KeyCode::Right,KeyCode::D]){ 
        player.translation.x += MOVMENT_SPEED * engine.delta_f32;
    }

    // handle mouse input
    if engine.mouse_state.just_pressed(MouseButton::Left){
        if let Some(mouse_location) = engine.mouse_state.location(){
            let label = format!("fire_{}", game_state.fire_index);
            game_state.fire_index += 1;
            //let fire: &mut Sprite = engine.add_sprite( label.clone(), "sprite/red-flame.png");
            let mut fire = engine.add_sprite( label.clone(), "sprite/red-flame.png");
            fire.translation = mouse_location;
            fire.collision = true;
            fire.scale = 0.5;
        }
    }

    // Reset score
    if engine.keyboard_state.just_pressed(KeyCode::R){
        game_state.score = 0;
        let score = engine.texts.get_mut("score").unwrap();
        score.value = format!("Score: {}", game_state.score);
    }
}
