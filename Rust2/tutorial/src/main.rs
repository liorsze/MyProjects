
use bevy::audio::PlaybackMode;
use rusty_engine::prelude::*;

#[derive(Resource)]
struct GameState{
    high_score: i32,
    current_score: i32,
    enemy_labels: Vec<String>,
    spawn_timer: Timer,
} 

impl Default for GameState {
    fn default() -> Self {
        Self {
            high_score: 0,
            current_score: 0,
            enemy_labels: vec![],
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

    let fire: &mut Sprite = game.add_sprite("fire", "sprite/red-flame.png");
    fire.translation = Vec2::new(300.0, 0.0);
    fire.collision = true;
    fire.scale = 0.5;
    

    game.add_logic(game_logic);
    game.run(GameState::default());
}

fn game_logic(engine: &mut Engine, game_state: &mut GameState) {
    engine.show_colliders = true;
    for event in engine.collision_events.drain(..){
        //println!("Collision event: {:#?}", event);
        if event.state == CollisionState::Begin && event.pair.one_starts_with("player"){
            // remove the sprite that the player collided with
            for lable in [event.pair.0, event.pair.1] {
                if lable != "player" {
                    engine.sprites.remove(&lable);
                }
            }

            game_state.current_score += 1;
            println!("Current score: {}", game_state.current_score);
        }
    }

    let player = engine.sprites.get_mut("player").unwrap();
    player.translation.x += 100.0 * engine.delta_f32;
}
