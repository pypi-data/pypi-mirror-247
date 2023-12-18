use crate::prelude::*;
use crate::MAIN_ENGINE;

use crate::ffi::python::Weapons;

use pyo3::exceptions::{PyEnvironmentError, PyValueError};
use pyo3::{pyfunction, PyResult, Python};

/// Sets a player's ammo.
#[pyfunction]
#[pyo3(name = "set_ammo")]
pub(crate) fn pyshinqlx_set_ammo(py: Python<'_>, client_id: i32, ammos: Weapons) -> PyResult<bool> {
    let maxclients = py.allow_threads(|| {
        let Some(ref main_engine) = *MAIN_ENGINE.load() else {
            return Err(PyEnvironmentError::new_err(
                "main quake live engine not set",
            ));
        };

        Ok(main_engine.get_max_clients())
    })?;

    if !(0..maxclients).contains(&client_id) {
        return Err(PyValueError::new_err(format!(
            "client_id needs to be a number from 0 to {}.",
            maxclients - 1
        )));
    }

    py.allow_threads(|| {
        #[cfg_attr(test, allow(clippy::unnecessary_fallible_conversions))]
        let mut opt_game_client = GameEntity::try_from(client_id)
            .ok()
            .and_then(|game_entity| game_entity.get_game_client().ok());
        opt_game_client
            .iter_mut()
            .for_each(|game_client| game_client.set_ammos(ammos.into()));
        Ok(opt_game_client.is_some())
    })
}

#[cfg(test)]
#[cfg(not(miri))]
mod set_ammo_tests {
    use super::pyshinqlx_set_ammo;
    use super::MAIN_ENGINE;
    use crate::ffi::c::game_client::MockGameClient;
    use crate::ffi::c::game_entity::MockGameEntity;
    use crate::ffi::python::Weapons;
    use crate::prelude::*;
    use crate::quake_live_engine::MockQuakeEngine;
    use mockall::predicate;
    use pretty_assertions::assert_eq;
    use pyo3::exceptions::{PyEnvironmentError, PyValueError};
    use pyo3::prelude::*;

    #[test]
    #[serial]
    fn set_ammo_when_main_engine_not_initialized() {
        MAIN_ENGINE.store(None);
        Python::with_gil(|py| {
            let result =
                pyshinqlx_set_ammo(py, 21, Weapons(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0));
            assert!(result.is_err_and(|err| err.is_instance_of::<PyEnvironmentError>(py)));
        });
    }

    #[test]
    #[serial]
    fn set_ammo_for_client_id_too_small() {
        let mut mock_engine = MockQuakeEngine::new();
        mock_engine.expect_get_max_clients().returning(|| 16);
        MAIN_ENGINE.store(Some(mock_engine.into()));

        Python::with_gil(|py| {
            let result =
                pyshinqlx_set_ammo(py, -1, Weapons(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0));
            assert!(result.is_err_and(|err| err.is_instance_of::<PyValueError>(py)));
        });
    }

    #[test]
    #[serial]
    fn set_ammo_for_client_id_too_large() {
        let mut mock_engine = MockQuakeEngine::new();
        mock_engine.expect_get_max_clients().returning(|| 16);
        MAIN_ENGINE.store(Some(mock_engine.into()));

        Python::with_gil(|py| {
            let result = pyshinqlx_set_ammo(
                py,
                666,
                Weapons(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            );
            assert!(result.is_err_and(|err| err.is_instance_of::<PyValueError>(py)));
        });
    }

    #[test]
    #[serial]
    fn set_ammo_for_existing_game_client() {
        let mut mock_engine = MockQuakeEngine::new();
        mock_engine.expect_get_max_clients().returning(|| 16);
        MAIN_ENGINE.store(Some(mock_engine.into()));

        let game_entity_from_ctx = MockGameEntity::from_context();
        game_entity_from_ctx.expect().returning(|_| {
            let mut mock_game_entity = MockGameEntity::new();
            mock_game_entity.expect_get_game_client().returning(|| {
                let mut mock_game_client = MockGameClient::new();
                mock_game_client
                    .expect_set_ammos()
                    .with(predicate::eq([
                        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                    ]))
                    .times(1);
                Ok(mock_game_client)
            });
            mock_game_entity
        });

        let result = Python::with_gil(|py| {
            pyshinqlx_set_ammo(
                py,
                2,
                Weapons(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
            )
        });
        assert_eq!(result.expect("result was not OK"), true);
    }

    #[test]
    #[serial]
    fn set_ammo_for_entity_with_no_game_client() {
        let mut mock_engine = MockQuakeEngine::new();
        mock_engine.expect_get_max_clients().returning(|| 16);
        MAIN_ENGINE.store(Some(mock_engine.into()));

        let game_entity_from_ctx = MockGameEntity::from_context();
        game_entity_from_ctx.expect().returning(|_| {
            let mut mock_game_entity = MockGameEntity::new();
            mock_game_entity
                .expect_get_game_client()
                .returning(|| Err(QuakeLiveEngineError::MainEngineNotInitialized));
            mock_game_entity
        });

        let result = Python::with_gil(|py| {
            pyshinqlx_set_ammo(py, 2, Weapons(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        });
        assert_eq!(result.expect("result was not OK"), false);
    }
}
